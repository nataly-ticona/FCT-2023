from django.shortcuts import render
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
#vista de un summoner
class SummonerView(View): # Django CBV with json response
    def get(self, request):
        summoner = cass.Summoner(name="ArYaNaMDA", region='EUW')
        print(summoner.profile_icon.url)
        return JsonResponse({"name": summoner.name, "level": summoner.level,"imagen":summoner.profile_icon.url})

def registerPage(request):
    form = CreateUserForm()

    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            cuenta = form.save()
            Usuario.objects.create(
                user=cuenta,
                nb_user=cuenta.username,
                email_user=cuenta.email,
                passwd_user = cuenta.password
            )
    return render(request, 'accounts/register.html', {
        'form':form
    })