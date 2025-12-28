from django.contrib import admin
from budget.models import Expense, ChatHistory, ChatConversations


# Register your models here.
admin.site.register(Expense)
admin.site.register(ChatHistory)
admin.site.register(ChatConversations)