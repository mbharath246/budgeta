from django.shortcuts import render, redirect
from django.urls import reverse
from users import forms

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # form.save()
            redirect(reverse('login'))
        else:
            print(form.errors)
    else:
        form = forms.SignupForm()
    return render(request, 'signup.html', {'form': form})