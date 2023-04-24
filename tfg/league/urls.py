from django.urls import path
from . import views

urlpatterns = [
    path('', views.SummonerView.as_view(), name='index'),
    path('register/', views.registerPage, name='register')
    
    ]