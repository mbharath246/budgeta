from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import datetime
from uuid import uuid4
from django.http import JsonResponse, StreamingHttpResponse
import logging as logger
from django.conf import settings

from budget.forms import AddExpenseForm
from budget.models import Expense, ChatConversations, ChatHistory
from budget.services.qdrant_service import qdrant_db
from budget.services.llm_client import llm


@login_required(login_url="/users/login/")
def home_view(request):
    category = request.GET.get("category")
    now = datetime.now()
    if category is None or category == "All":
        expense_details = Expense.objects.filter(user_id=request.user.id, date__year=now.year, date__month=now.month).all()
    elif category in ("Personal", "Home", "Other"):
        expense_details = Expense.objects.filter(
            user_id=request.user.id, category=category, date__year=now.year, date__month=now.month
        ).all()
    else:
        expense_details = Expense.objects.filter(user_id=request.user.id, date__year=now.year, date__month=now.month).all()

    paid = request.GET.get("paid")
    if paid:
        if paid is None or paid == "All":
            expense_details = expense_details.filter(user_id=request.user.id).all()
        elif paid in ("UPI", "Cash", "Credit Card", "Debit Card", "Gift Card", "Net Banking", "Others"):
            expense_details = expense_details.filter(
                user_id=request.user.id, paid=paid
            ).all()
    
    amount = sum(expense_details.values_list('amount', flat=True))
    return render(
        request,
        "home/index.html",
        {
            "expense_details": expense_details,
            "active_link": "home",
            "selected_category": category,
            "paid_by": paid,
            "amount": amount
        },
    )


@login_required(login_url="/users/login/")
def add_expense(request):
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user
            data = form.save()
            
            if settings.AI_ENABLED:
                payload_text = {
                    "expense name": data.name,
                    "amount": float(data.amount),
                    "category": data.category,
                    "date": data.date.strftime("%d/%m/%Y, %H:%M:%S"),
                    "description": data.description,
                    "paid_by": data.paid
                }
                metadata = {
                    **payload_text,
                    "user_id": request.user.id
                }
                print(payload_text)
                qdrant_db.store_items(data.id, texts=[str(payload_text)], metadatas=[metadata])
                
            return redirect("/budget/index")
        else:
            print(form.errors)
    form = AddExpenseForm()
    return render(request, "home/add-expense.html", {"form": form, "active_link": "add-expense"})



@login_required(login_url="/users/login/")
def monthly_expenses(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    selected_category = request.GET.get('category')
    paid = request.GET.get('paid')
    now = datetime.now()

    months_dict = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    if selected_month and selected_year:
        expenses = Expense.objects.filter(
            user_id=request.user.id,
            date__year=selected_year,
            date__month=months_dict[selected_month]
        )
    else:
        selected_month = now.strftime("%B")
        selected_year = now.year
        expenses = Expense.objects.filter(
            user_id=request.user.id,
            date__year=now.year,
            date__month=now.month
        )
    if selected_category:
        if selected_category == "All":
            expenses = expenses.filter(user_id=request.user.id).all()
        elif selected_category in ("Personal", "Home", "Other"):
            expenses = expenses.filter(
                user_id=request.user.id, category=selected_category
            ).all()

    if paid:
        if paid == "All":
            expenses = expenses.filter(user_id=request.user.id).all()
        elif paid in ("UPI", "Cash", "Credit Card", "Debit Card", "Gift Card", "Net Banking", "Others"):
            expenses = expenses.filter(
                user_id=request.user.id, paid=paid
            ).all()

    amount = sum(expenses.values_list('amount', flat=True))

    context = {
        'expenses': expenses,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'selected_category': selected_category,
        'paid_by': paid,
        'amount': amount,
        "active_link": "monthly-expenses",
    }
    return render(request, "home/monthly.html", context)


@login_required(login_url="/users/login/")
def yearly_expenses(request):
    selected_year = request.GET.get('year')
    if not selected_year:
        selected_year = datetime.now().year

    monthly_expenses = (
        Expense.objects.filter(date__year=selected_year, user_id=request.user.id)
        .values('date__month')
        .annotate(total_amount=Sum('amount'))
        .order_by('date__month')
    )

    month_names = {
        "1": "January", "2": "February", "3": "March",
        "4": "April", "5": "May", "6": "June",
        "7": "July", "8": "August", "9": "September",
        "10": "October", "11": "November", "12": "December"
    }
    monthly_summary = {
        "January": 0, "February": 0, "March": 0, "April": 0,
        "May": 0, "June": 0, "July": 0, "August": 0, "September": 0,
        "October": 0, "November": 0, "December": 0
    }
    amount = float()
    for item in monthly_expenses:
        monthly_summary[month_names[str(item['date__month'])]] = item['total_amount']
        amount += float(item["total_amount"])
   
    context = {
        'monthly_summary': monthly_summary,
        'selected_year': selected_year,
        'amount': amount,
        "active_link": "yearly-expenses",
    }

    return render(request, 'home/yearly.html', context)


@login_required(login_url="/users/login/")
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user_id=request.user.id)
    if request.method == "POST":
        form = AddExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            data = form.save()
            
            if settings.AI_ENABLED:
                payload_text = {
                    "expense name": data.name,
                    "amount": float(data.amount),
                    "category": data.category,
                    "date": data.date.strftime("%d/%m/%Y, %H:%M:%S"),
                    "description": data.description,
                    "paid_by": data.paid
                }
                metadata = {
                    **payload_text,
                    "user_id": request.user.id
                }
                print(payload_text)
                qdrant_db.store_items(data.id, texts=[str(payload_text)], metadatas=[metadata])
                
            return redirect('index')
    else:
        form = AddExpenseForm(instance=expense)
    
    return render(request, 'home/edit-expense.html', {'form': form})


@login_required(login_url="/users/login/")
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user_id=request.user.id)
    if request.method == "POST":
        expense.delete()
        
        if settings.AI_ENABLED:
            qdrant_db.delete_item(expense_id)
            
        return redirect('index')
    
    return render(request, 'home/delete-expense.html', {'expense': expense})


@login_required(login_url="/users/login")
def chatbot(request, cid=None):
    context = {
        "active_link": "chatbot",
        "cid": cid
    }
    
    if request.method == 'POST':
        query = request.POST.get("query")
        user_id = request.user.id
        current_chat = ChatConversations.objects.filter(conversation_id=cid, user_id=user_id).first()
        if not current_chat:
            current_chat = ChatConversations(
                user_id=request.user,
                conversation_id=uuid4(),
                chat_name=query if len(query) < 100 else query[:60] + "..."
            )
            current_chat.save()
        
        conversation_id = current_chat.conversation_id
        
        print(conversation_id, current_chat.create_time)
        search_results = qdrant_db.search_points(query, user_id)
        logger.info(f"found retrieved docs {len(search_results)}")
        print(f"found retrieved docs {len(search_results)}")
        prompt = f"""
            You are an intelligent Expense Assistant.

            Your task is to respond appropriately based on the user's intent.

            ==============================
            INTENT RULES (MANDATORY)
            ==============================

            1. If the user query is conversational or generic
            (examples: "hi", "hello", "how are you", "what can you do"):
            - Respond with ONLY the **Answer** section.
            - DO NOT include "Key Details", tables, lists, or extra sections.
            - All the expense details are in rupees only.

            2. If the user query is related to expenses, finance, totals, summaries,
            categories, dates, comparisons, or calculations:
            - Respond with **Answer + Key Details**.
            - Use bullet points or tables inside Key Details where applicable.

            3. Never include empty or generic Key Details.
            4. Do not add sections unless they provide meaningful information.

            ==============================
            OUTPUT FORMAT
            ==============================

            For conversational queries:

            ## ✅ Answer
            <short, friendly response>

            --------------------------------

            For financial / expense queries:

            ## ✅ Answer
            <direct summary sentence>

            ## 📌 Key Details
            <structured details, bullet points or tables>

            ==============================
            CONTEXT
            ==============================

            User Question:
            {query}

            Retrieved Expense Records:
            {search_results}
        """

        response = llm.invoke(prompt)
        
        chat_history = ChatHistory(
            user_id = request.user,
            conversation_id = current_chat,
            question = query,
            response = response.content,
        )
        chat_history.save()
        
        context["cid"] = conversation_id
        return JsonResponse({
            "message": response.content,
            "cid": str(current_chat.conversation_id)
        })
    
    return render(request, 'chatbot/chatbot.html', context)
