from django.urls import path
from budget import views


urlpatterns = [
    path('index/', views.header_view, name="index"),
    path('add/', views.add_expense, name="add")
]
