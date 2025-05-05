from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Expense Name'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Spending amount'))
    category = models.CharField(max_length=30, verbose_name=_('Type of the Expense ex: Personal, Home, etc.'))
    date = models.DateTimeField(auto_now=True, help_text="The date of the expense.", editable=True)
    description = models.TextField(verbose_name=_('Description for expense.'))
    
    class Meta:
        ordering = ['-date']