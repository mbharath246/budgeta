from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users import forms

# Create your views here.
def login_view(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is not None and user.is_authenticated:
                login(request, user)
                return redirect(reverse('index'))
            
    return render(request, 'users/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
        else:
            print("Form errors:", form.errors)
    else:
        form = forms.SignupForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required(login_url="/users/login/")
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))