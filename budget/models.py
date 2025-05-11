from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Users

# Create your models here.
class Expense(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category_choices = (
            ('Personal', 'Personal'),
            ('Home', 'Home'),
            ('Other', 'Other')
        )
        
    category = models.CharField(max_length=30, help_text=_("Type of the Expense ex: Personal, Home, etc."), choices=category_choices)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    paid_choices = {
        "UPI":"UPI",
        "Cash": "Cash",
        "Credit Card": "Credit Card",
        "Online Payments": "Online Payments", 
        "Others": "Others"
    }
    paid = models.CharField(max_length=30, verbose_name=_('Payment Type'), choices=paid_choices)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f'{self.user_id} Spending: {self.name} '