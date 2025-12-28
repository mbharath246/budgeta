from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from budget.models import Expense


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
        
        category_choices = (
            ('Personal', 'Personal'),
            ('Home', 'Home'),
            ('Other', 'Other')
        )
        
        paid_choices = {
            "UPI":"UPI",
            "Cash": "Cash",
            "Credit Card": "Credit Card",
            "Online Payments": "Online Payments", 
            "Others": "Others"
        }
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control ", "placeholder":"Expense Name"}),
            "amount": forms.TextInput(attrs={"class": "form-control", "placeholder":'Spending amount'}),
            "category": forms.Select(attrs={"class": "form-control", "placeholder":'Type of the Expense ex: Personal, Home, etc.'}, choices=category_choices),
            "date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local", "placeholder":"The date of the expense."}
            ),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder":'Description for expense.'}),
            "paid": forms.Select(attrs={"class": "form-control", "placeholder":'Type of the Expense ex: Personal, Home, etc.'}, choices=paid_choices)
        }

        exclude = ['user_id']
        