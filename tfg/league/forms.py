from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms

from .models import League_User

class OrderForm(ModelForm):
    class Meta:
        model = League_User
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['nb_user','email_user','password1','password2']

