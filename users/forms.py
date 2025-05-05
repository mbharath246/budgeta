from django import forms
from users import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignupForm(forms.ModelForm):
    class Meta:
        model = models.Users
        fields = ['name', 'email', 'phone', 'password']
        # exclude = ['id']