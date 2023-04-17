from django.shortcuts import render
from django.http import HttpResponse
#Librerias para 'Cassiopeia'
from django_cassiopeia import cassiopeia as cass
from django.http import JsonResponse
from django.views import View

#vista de un summoner
class SummonerView(View): # Django CBV with json response
    def get(self, request):
        summoner = cass.Summoner(name="CENTRIFUGADORYAN", region='EUW')
        return JsonResponse({"name": summoner.name, "level": summoner.level})
