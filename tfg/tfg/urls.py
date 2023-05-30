from django.contrib import admin
from django.urls import include,path
# para poder añadir imagenes importamos lo siguiente y el static de la variable
from django.conf.urls.static import static
# para que funcione el css y js de los archivos cuando el debug esta en false 
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlace la app league
    path('league/', include('league.urls')),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# conectando el error 404
handler404 = "league.views.error_404"
# handler500 = "league.views.error_404"