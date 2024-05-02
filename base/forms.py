from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mail

class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['receiver', 'title', 'content']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50) #Is now required
    last_name = forms.CharField(max_length=50) #Is now required

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']