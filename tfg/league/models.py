from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
#Libreria importada para registro-login
from django.contrib.auth.models import User as User_Default


# Create your models here.

class User(models.Model):
    user                =models.OneToOneField(User_Default,null=True,blank=True, on_delete=models.CASCADE)
    email_user          =models.EmailField(_("email address"), unique=True)
    nb_user             =models.CharField(max_length=200,unique=True)
    passwd_user         =models.CharField(max_length=200)
    nick_name_user      =models.CharField(max_length=200)
    photo_user          =models.ImageField(default="/imagen/users/profile.png", upload_to='imagen/users', null=True, blank=False)
    date_joined_user    =models.DateTimeField(default=timezone.now)
    #Falta categoria de vip/common
    #Falta is_active?

    def __str__(self):
        return self.nb_user

class Token(models.Model):
    user = models.ForeignKey(User_Default, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.token

# Revisar validacion de correo en los models
class Post(models.Model):
    user_post      = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    champion       = models.CharField(max_length=200)
    tittle_post    = models.CharField(max_length=200)
    keystone       = models.CharField(max_length=200)
    items1         = models.CharField(max_length=200)
    items2         = models.CharField(max_length=200)
    items3         = models.CharField(max_length=200)
    items4         = models.CharField(max_length=200)
    items5         = models.CharField(max_length=200)
    items6         = models.CharField(max_length=200)
    summoner_spells1 = models.CharField(max_length=200)
    summoner_spells2 = models.CharField(max_length=200)
    # habilities 
    def __str__(self):
        return self.tittle_post + ', ' + self.champion  + ', ' + self.user_post.nb_user