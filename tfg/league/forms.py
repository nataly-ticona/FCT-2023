from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms

from .models import User as Usuario
from .models import Post


class OrderForm(ModelForm):
    class Meta:
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ['user', 'passwd_user', 'date_joined_user']
    
class CreatePost(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user_post', 'champion']