import requests
from tfg.settings import CASSIOPEIA_DEFAULT_REGION
from tfg.settings import CASSIOPEIA_RIOT_API_KEY
from tfg.settings import MEDIA_ROOT

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Token, User as Usuario
# imagenes
import os
# libreria del LOL
from cassiopeia import Champion, Champions, Queue, Patch
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
#paginador para el ranking
from django.core.paginator import Paginator
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
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
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
    users = Usuario.objects.all
    context = {
        "champions":champions,
        "users": users,
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

def detailChampion(request, champion_name):
    champion = Champion(name=champion_name, region=CASSIOPEIA_DEFAULT_REGION)
    runes = cassiopeia.Runes(region=CASSIOPEIA_DEFAULT_REGION).keystones
    base_dir = MEDIA_ROOT
    path_skins = str(base_dir) + "/imagen/league/skins" 
    path_abilities = str(base_dir) + "/imagen/league/spell"
    path_passive = str(base_dir) + "/imagen/league/passive"
    img_skins = os.listdir(path_skins)  
    img_abilities = os.listdir(path_abilities)
    img_passives = os.listdir(path_passive)

    context={'champion':champion, 'runes': runes,'img_champion_skin':img_skins, 'img_champion_abilities':img_abilities, 'img_champion_passives':img_passives}
    return render(request, 'league/detail_champion.html', context)

def userView(request, user_name):
    usuario = Usuario.objects.get(nb_user=user_name)
    context = {'usuario': usuario}
    return render(request, 'accounts/user_public.html', context)

@login_required(login_url='login')
def myAccount(request):
    user = request.user.user
    context={'user':user,}
    return render(request, 'accounts/my_account.html', context)


def ranking(request):
    page_amount=25
    url = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={CASSIOPEIA_RIOT_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        challenger =response.json()['entries']
        challenger.sort(key=extract_time, reverse=True)
        paginator = Paginator(challenger, page_amount)  # Show 25 values per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        best = challenger[0:3]
    return render(request, 'league/ranking.html',{
        "challenger":challenger,
        "page_obj":page_obj,
        "page_amount":page_amount,
        "best":best,
    })
#Para ordenar por lp
def extract_time(json):
    try:
        return int(json['leaguePoints'])
    except KeyError:
        return 0

# vista tier list
def tier_list(request):
    patch = Patch.latest(region=CASSIOPEIA_DEFAULT_REGION)
    champions = Champion(region=CASSIOPEIA_DEFAULT_REGION, api_key=CASSIOPEIA_RIOT_API_KEY)

    for champion in champions:
        champion_id = champion.id
        win_rate = champion.win_rate(patch=patch, champion_id=champion_id)
    print(f"{champion.name}: {win_rate}%")

    context = {
        # "champions":champions
    }
    return render(request, 'league/tier_list.html', context)

# creando el error 404
def error_404 (request, exception):
    return render(request, '404.html')
