from django.contrib import admin
from django.urls import include,path
# para poder añadir imagenes importamos lo siguiente y el static de la variable
from django.conf.urls.static import static
# para que funcione el css y js de los archivos cuando el debug esta en false 
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlace la app league
    path('league/', include('league.urls')),  
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# conectando el error 404
error404 = "helpers.views.error_404"