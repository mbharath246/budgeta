from django.urls import path
from budget import views


urlpatterns = [
    path('index/', views.home_view, name="index"),
    path('add/', views.add_expense, name="add"),
    path('month/', views.monthly_expenses, name="month"),
    path('year/', views.yearly_expenses, name="year"),
    path('edit/<int:expense_id>/', views.edit_expense, name="edit"),
    path('delete/<int:expense_id>/', views.delete_expense, name="delete"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path("chatbot/<uuid:cid>/", views.chatbot, name="chatbot_with_id"),
]
