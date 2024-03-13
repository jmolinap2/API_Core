from django.utils.deprecation import MiddlewareMixin
import sys
from django.contrib.auth import authenticate
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
#drf\middleware.py

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('headers que llegan a RequestLoggingMiddleware: ', request.headers)
        # Obtenemos la dirección IP del cliente
        ip_address = request.META.get('REMOTE_ADDR', '')
        # Si hay un usuario autenticado, lo obtenemos
        user = request.user if request.user.is_authenticated else None
        full_path = request.build_absolute_uri()
        # Imprimimos la información en color
        if user !=None:
            print(f"\033[92mRequest from {ip_address}, User: {user}, Path: {full_path}\033[0m", file=sys.stdout)
        else:
            print(f"\033[91mRequest from {ip_address}, User: anonymous, Path: {full_path}\033[0m", file=sys.stdout)

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado utilizando TokenAuthentication de DRF
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Token '):
            try:
                print(f'TokenAuthenticationMiddleware')
                key = auth.split(' ')[1]
                token = Token.objects.get(key=key)
                request.user = token.user
                print(f'Token:  {token}')
                print(f'user:  {request.user}')
            except Token.DoesNotExist:
                request.user = None

        response = self.get_response(request)
        return response