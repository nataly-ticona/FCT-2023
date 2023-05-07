# from django.http import HttpResponse
#Librerias para 'Cassiopeia'
# from django.http import JsonResponse
# from django.views import View
# import requests
# from django.core import serializers
#Libreria importada para registro-login

from tfg.settings import CASSIOPEIA_DEFAULT_REGION
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Token, User as Usuario
# libreria del LOL
from cassiopeia import Champion, Champions
from django_cassiopeia import cassiopeia 
# mensajes de aviso (usuario creado, documento eliminado, etc)
from django.contrib import messages
# autentificacion, login, logout metodos
from django.contrib.auth import authenticate, login, logout
# restriccion de login en paginas
from django.contrib.auth.decorators import login_required
# email registration
from django.core.mail import EmailMessage
from django.conf import settings
# crea un temepleate con el mensaje y el nommbre del usuario
# from django.template.loader import render_to_string


from datetime import datetime, timedelta
import uuid

from django.http import HttpResponse
# tokens django
# from rest_framework import generics
# from .serializers import UserSerializer

def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            cuenta = form.save()
            
            # obtenemos datos y los limpiamos para no tener el codigo por defecto
            nombre_user = form.cleaned_data.get('username')            
            messages.success(request, 'Has creado un usuario '+ nombre_user + '! :D')
            email = EmailMessage(
                'Bienvenido a Wikigames!', 
                'Gracias por confiar en esta conmunidad',
                settings.EMAIL_HOST_USER,
                [cuenta.email],)
            email.fail_silently=False
            email.send()

            Usuario.objects.create(
                user=cuenta,
                nb_user=cuenta.username,
                email_user=cuenta.email,
                passwd_user = cuenta.password
            )
            return redirect('login')          
    return render(request, 'accounts/register.html', {
        'form':form
    })

def loginPage(request):
    if request.method == 'POST':
        username_login = request.POST.get('username')
        password_login = request.POST.get('password')

        user = authenticate(request, username = username_login, password = password_login)

        # el usuario es valido y redirecciona al index
        if user is not None:
            login(request, user)
            if request.POST.get('remember-me'):
                # destruir el token anterior asociada al usuario
                try:
                    Token.objects.get(user=user).delete()
                except Token.DoesNotExist:
                    pass
                # generar token y almacenarlo
                token = str(uuid.uuid4())

                expire_date = datetime.now() + timedelta(days=30)
                Token.objects.create(user=user, token=token, expire_date=expire_date)
                # set cookie
                response = redirect('index')
                response.set_cookie('remember_me_token', token, expires=expire_date)
                return response
            
            return redirect('index')
        else:
            messages.info(request, 'El nombre del usuario o la contraseña es incorrecta')

    context ={}
    return render(request, 'accounts/login.html',context )

def logoutPage(request):
    # obtener cookie
    token = request.COOKIES.get('remember_me_token')
    response = redirect('index')
    if token is not None:
        try:
            #eliminar registro del token
            Token.objects.get(token=token).delete()
        except Token.DoesNotExist:
            pass
        #destruir cookie
        response.delete_cookie('remember_me_token')
    #logout
    logout(request)
    return response


def index(request):
    champions = Champions(region=CASSIOPEIA_DEFAULT_REGION)
    context = {
        "champions":champions
    }
    return render(request, 'accounts/index.html', context)

@login_required(login_url='login')
def privatePage(request):
    context={}
    return render(request, 'accounts/private.html', context)

@login_required(login_url='login')
def accountSettings(request):
    user = request.user.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
    
    context={'user':user, 'form':form}
    return render(request, 'accounts/account_settings.html', context)


def detaiChampion(request, champion_name):
    champion = Champion(name=champion_name, region=CASSIOPEIA_DEFAULT_REGION)
    context={'champion':champion}
    return render(request, 'accounts/detail_champion.html', context)