import requests
from tfg.settings import CASSIOPEIA_DEFAULT_REGION
from tfg.settings import CASSIOPEIA_RIOT_API_KEY
from tfg.settings import MEDIA_ROOT

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Token,Post, User as Usuario

# imagenes
import os
# libreria del LOL
from cassiopeia import Champion, Champions, Queue, Patch, Summoner, Rank, Tier, Division
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
# No almacenar datos al hacer un redirect
from django.http import HttpResponse, HttpResponseRedirect
# tokens django
# from rest_framework import generics
# from .serializers import UserSerializer
# traduccion de textos
from googletrans import Translator

def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)

        # validar que el email no se repite
        usuarioRepetido = Usuario.objects.filter(nb_user=request.POST.get('username'))
        if(usuarioRepetido.__len__()>0):
            messages.info(request, 'El nombre de usuario ya existe')
            return render(request, 'accounts/register.html', {'form':form})
        emailRepetido = Usuario.objects.filter(email_user=request.POST.get('email'))
        if(emailRepetido.__len__()>0):
            messages.info(request, 'El correo proporcionado ya existe')
            return render(request, 'accounts/register.html', {'form':form})
        
        if form.is_valid():
            cuenta = form.save()
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
            # user = authenticate(request, username = cuenta.username, password = cuenta.password)
            login(request, cuenta)
            return redirect('index')
        else:
            messages.info(request, f'Contraseña inválida. \n\nLa contraseña debe tener al menos 7 caracteres. \nTener al menos un valor numérico. \nNo puede ser similar al nombre de usuario.' )
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
    translator = Translator()
    champion = Champion(name=champion_name, region=CASSIOPEIA_DEFAULT_REGION)
    runes = cassiopeia.Runes(region=CASSIOPEIA_DEFAULT_REGION).keystones
    base_dir = MEDIA_ROOT
    
    path_skins = str(base_dir) + "/imagen/league/skins" 
    path_abilities = str(base_dir) + "/imagen/league/spell"
    path_passive = str(base_dir) + "/imagen/league/passive"
    path_item = str(base_dir) + "/imagen/league/item"
    img_skins = os.listdir(path_skins)  
    img_abilities = os.listdir(path_abilities)
    img_passives = os.listdir(path_passive)
    img_items = os.listdir(path_item)
    lore = translator.translate(champion.lore, dest='es')
    title = translator.translate(champion.title, dest='es')
    post_champion = Post.objects.filter(champion=champion_name)
    
    context={'champion':champion, 
            'runes': runes,
            'img_champion_skin':img_skins, 
            'img_champion_abilities':img_abilities, 
            'img_champion_passives':img_passives, 
            'img_champion_items':img_items,
            'lore':lore,
            'title':title,
            'posts_champion':post_champion,
            }
    return render(request, 'league/detail_champion.html', context)

def userView(request, user_name):
    currentUsername = request.user
    user = Usuario.objects.get(nb_user=user_name)
    posts=Post.objects.filter(user_post=user)
    champions = Champions(region=CASSIOPEIA_DEFAULT_REGION)
    context = {
        'user': user, 
        'currentUser':currentUsername,
        'posts':posts,
        'champions':champions
    }
    return render(request, 'accounts/user_public.html', context)


# creando el error 404
def error_404(request, exception):
    return render(request, '404.html')

def ranking(request):
    page_amount=25
    url = f'https://euw1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={CASSIOPEIA_RIOT_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        challenger =response.json()['entries']
        challenger.sort(key=extract_time, reverse=True)
        paginator = Paginator(challenger, page_amount)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        best = challenger[0:3]
    else:   
        return render(request, '404.html')
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

@login_required(login_url='login')
def createPost(request, champion_name):
    user_data = request.user
    user = Usuario.objects.get(nb_user=user_data.username)
    keystone = cassiopeia.Runes(region=CASSIOPEIA_DEFAULT_REGION).keystones
    base_dir = MEDIA_ROOT
    path_item = str(base_dir) + "/imagen/league/item" 
    path_spells = str(base_dir) + "/imagen/league/summoner_spells" 
    img_items = os.listdir(path_item)  
    img_spells = os.listdir(path_spells)
    titulo = Post.objects.filter(tittle_post=request.POST.get('tittle_post'))
    
    if request.method == "POST":
        if(titulo.__len__()==0):
            # create a form instance and populate it with data from the request:
            form = CreatePost(request.POST)
            # check whether it's valid:
            if form.is_valid():
            #    form.save()
            #    si ponemos form.save se guardan dos
                data_form =  form.save(commit=False)
                # obtenemos datos y los limpiamos para no tener el codigo por defecto
                Post.objects.create(
                    user_post = user,
                    champion = champion_name,
                    tittle_post = data_form.tittle_post,
                    keystone = data_form.keystone,
                    items1 = data_form.items1,
                    items2 = data_form.items2,
                    items3 = data_form.items3,
                    items4 = data_form.items4,
                    items5 = data_form.items5,
                    items6 = data_form.items6,
                    summoner_spells1 = data_form.summoner_spells1,
                    summoner_spells2 = data_form.summoner_spells2
                )
                return redirect('posts')   
        else: 
            messages.info(request, f'Ya existe el titulo del post: {request.POST.get("tittle_post")}') 
    form = CreatePost()

    return render(request, "accounts/createPost.html", {"form": form,
                                                        'items':img_items, 
                                                        "spells":img_spells,
                                                        'keystone':keystone[:len(keystone)-6],
                                                        })

def posts(request):
    post = Post.objects.all
    champions = Champions(region=CASSIOPEIA_DEFAULT_REGION)
    return render(request, 'accounts/post.html', {'posts':post,'champions':champions})

def privacy_policy(request):
    return render(request, 'accounts/privacy_policy.html')

def cookies_policy(request):
    return render(request, 'accounts/cookies_policy.html')

def legal_warning(request):
    return render(request, 'accounts/legal_warning.html')


def summoners_list(request,summoner_name):
    summoner = Summoner(name=summoner_name,region=CASSIOPEIA_DEFAULT_REGION)
    queue_summoner = Queue.ranked_flex_fives
    rank_summoner = summoner.match_history(start_time="0",end_time="20", puuid=summoner.puuid,continent="europe")
    rank_summ = Rank()
    context = {
        'rank': rank_summoner,
        'queue': queue_summoner,
        'summoner':summoner,
    }

    return render(request, 'league/detail_summoner.html',context)
