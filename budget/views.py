from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import datetime

from budget.forms import AddExpenseForm
from budget.models import Expense


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
        elif paid in ("UPI", "Cash", "Credit Card", "Online Payments", "Others"):
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
            form.save()
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
        elif paid in ("UPI", "Cash", "Credit Card", "Online Payments", "Others"):
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
            form.save()
            return redirect('index')  # Redirect to expense list page
    else:
        form = AddExpenseForm(instance=expense)
    
    return render(request, 'home/edit-expense.html', {'form': form})


@login_required(login_url="/users/login/")
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user_id=request.user.id)
    if request.method == "POST":
        expense.delete()
        return redirect('index')
    
    return render(request, 'home/delete-expense.html', {'expense': expense})