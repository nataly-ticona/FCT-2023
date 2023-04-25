from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
#Libreria importada para registro-login
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
    user                =models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    email_user          =models.EmailField(_("email address"), unique=True)
    nb_user             =models.CharField(max_length=200,unique=True)
    passwd_user         =models.CharField(max_length=200)
    nick_name_user      =models.CharField(max_length=200)
    photo_user          =models.ImageField(upload_to='imagen', null=True, blank=False)
    date_joined_user    =models.DateTimeField(default=timezone.now)
    #Falta categoria de vip/common
    #Falta is_active?

    def __str__(self):
        return self.nb_user

# Revisar validacion de correo en los models