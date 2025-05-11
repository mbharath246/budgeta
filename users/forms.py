from django import forms
from users import models
from django.contrib.auth.hashers import check_password


class SignupForm(forms.ModelForm):
    class Meta:
        model = models.Users
        fields = ['name', 'email', 'phone', 'password']
        # exclude = ['id']
        
    def save(self, commit = True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance
        
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        print("username", username)
        user = models.Users.objects.filter(email=username)
        print(user)
        if not(username and user.exists()):
            raise forms.ValidationError('Invalid Username')
        return username
    
    def clean_password(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            user = models.Users.objects.get(email=username)
        except models.Users.DoesNotExist:
            raise forms.ValidationError("Invalid username or password.")

        if not check_password(password, user.password):
            raise forms.ValidationError("Invalid username or password.")

        return cleaned_data