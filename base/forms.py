from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mail

class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50) #Is now required
    last_name = forms.CharField(max_length=50) #Is now required

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']