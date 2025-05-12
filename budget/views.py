from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from budget.forms import AddExpenseForm
from budget.models import Expense


@login_required(login_url="/users/login/")
def header_view(request):
    expense_details = Expense.objects.filter(user_id=request.user.id).all()
    return render(request, 'home/index.html', {'expense_details': expense_details, 'active_link': 'home'})


@login_required(login_url="/users/login/")
def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user
            form.save()
            print(form.cleaned_data)
            
            return redirect('/budget/index')
        else:
           print(form.errors)
    form = AddExpenseForm()
    return render(request, 'home/add-expense.html', {'form':form, 'active_link': 'add-expense'})