from django.utils import timezone
from django.contrib.auth import authenticate, login
from .models import Token

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #obtener cookie
        token = request.COOKIES.get('remember_me_token')
        if token is not None:
            try:
                #si hay cookie, obtener el registro en la base de datos
                token_obj = Token.objects.get(token=token)
                if token_obj.expire_date>timezone.now():
                    #si el registro existe autentica con el usuario enlazado al token
                    user = authenticate(request, username=token_obj.user.username, password=None)
                    if user is not None:
                        login(request, user)
                else:
                    token_obj.delete()
            except Token.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
