from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Users


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
        "Debit Card": "Debit Card",
        "Gift Card": "Gift Card",
        "Net Banking": "Net Banking", 
        "Others": "Others"
    }
    paid = models.CharField(max_length=30, verbose_name=_('Payment Type'), choices=paid_choices)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f'{self.user_id} Spending: {self.name}'
    
      
class ChatConversations(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    conversation_id = models.UUIDField(unique=True)
    chat_name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    
    
class ChatHistory(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    conversation_id = models.ForeignKey(ChatConversations, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    response = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    