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
from .models import League_User as Usuario
from .forms import OrderForm,CreateUserForm

#vista de un summoner
class SummonerView(View): # Django CBV with json response
    def get(self, request):
        summoner = cass.Summoner(name="ArYaNaMDA", region='EUW')
        print(summoner.profile_icon.url)
        return JsonResponse({"name": summoner.name, "level": summoner.level,"imagen":summoner.profile_icon.url})






#Formulario creacion de formulario
def registerPage(request):
    #inciamos el objeto para crear fomularios
    form = UserCreationForm()
    #Comprobamos que hay POST
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Usuario.objects.create(user=usuario)

    context = {'form':form}
    return render(request,'accounts/register.html',context)








# def registerPage(request):
#     context = {}
#     return render(request,'accounts/register.html',context)


