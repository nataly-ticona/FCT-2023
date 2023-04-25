from django.shortcuts import render, redirect
from django.http import HttpResponse
#Librerias para 'Cassiopeia'
from django_cassiopeia import cassiopeia as cass
from django.http import JsonResponse
from django.views import View
import requests
#
from django.core import serializers
#Libreria importada para registro-login
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .models import User as Usuario

# mensajes de aviso (usuario creado, documento eliminado, etc)
from django.contrib import messages

# autentificacion, login, logout metodos
from django.contrib.auth import authenticate, login, logout
# restriccion de login en paginas
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, 'accounts/index.html', context)

def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            cuenta = form.save()
            Usuario.objects.create(
                user=cuenta,
                nb_user=cuenta.username,
                email_user=cuenta.email,
                passwd_user = cuenta.password
            )
            # obtenemos datos y los limpiamos para no tener el codigo por defecto
            nombre_user = form.cleaned_data.get('username')
            messages.success(request, 'Has creado un usuario '+ nombre_user + '! :D')
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
            return redirect('index')
        else:
            messages.info(request, 'El nombre del usuario o la contraseña es incorrecta')

    context ={}
    return render(request, 'accounts/login.html',context )

def logoutPage(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def privatePage(request):
    context={}
    return render(request, 'accounts/private.html', context)
#vista de un summoner
# class SummonerView(View): # Django CBV with json response
#     def get(self, request):
#         summoner = cass.Summoner(name="ArYaNaMDA", region='EUW')
#         print(summoner.profile_icon.url)
#         return JsonResponse({"name": summoner.name, "level": summoner.level,"imagen":summoner.profile_icon.url})

