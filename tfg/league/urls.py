from django.urls import path
# Import para recuperar la contraseña
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('private/', views.privatePage, name='private'),
    path('user/<str:user_name>', views.userView, name='user'),
    path('accountsettings/', views.accountSettings, name='accountsettings'),
    path('champion/<str:champion_name>/', views.detailChampion, name='detail'),
    path('ranking/', views.ranking, name='ranking'),
    #Url de la tierList
    path('tier_list/',views.tier_list, name="tier_list"),
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
    path('create-post/<str:champion_name>/', views.createPost, name='createPost'),
    path('posts/', views.posts, name='posts'),
    path('privacy-policy/', views.privacy_policy, name='privacyPolicy'),
    path('cookies-policy/', views.cookies_policy, name='cookiesPolicy'),
    path('legal_warning/', views.legal_warning, name='legalWarning'),

    #Listado de summoners
    path('summoner/<str:summoner_name>/',views.summoners_list, name='detail_summoner'),
    ]
