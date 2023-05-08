from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('private/', views.privatePage, name='private'),
    path('accountsettings/', views.accountSettings, name='accountsettings'),
    
   path('<str:champion_name>/', views.detaiChampion, name='detail'),
   
   #url's para recuperar la contraseña
    #vista para introducir el correo y asi cambiar a contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"), name='reset_password'),
    #Confirmacion de que se puede cambiar la contraseña
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_done.html"), name='password_reset_done'),
    #vista que nos muestra el formulario por el que se pasara el id codificado del usuario(seguro) y un token donde se almacena el cambio de contraseña
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password_form.html"), name='password_reset_confirm'),
    #Vista que nos confirma que nuestra contraseña se ha cambiado
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_complete.html"), name='password_reset_complete'),
    #dirigirse a los setting y configuar la parte SMTP
   
    ]
