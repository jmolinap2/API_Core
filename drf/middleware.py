from django.utils.deprecation import MiddlewareMixin
import sys
from django.contrib.auth import authenticate
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
#drf\middleware.py

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtener la dirección IP del cliente
        ip_address = request.META.get('REMOTE_ADDR', '')
        ip_origin = request.headers.get('Origin')
        
        # Determinar el tipo de acción
        action = self.get_action(request)
        
        # Obtener el usuario autenticado, si lo hay
        user = request.user if request.user.is_authenticated else None
        full_path = request.build_absolute_uri()
        
        # Construimos el mensaje de registro
        
        
        # Imprimimos el mensaje en color
        print(action, file=sys.stdout)

        if user is not None:
            message = f"\033[92m from CORS: {ip_origin}, User: {user}, Path: {full_path}\033[0m"
        else:
            message = f"\033[91m from CORS: {ip_origin}, User: anonymous, Path: {full_path}\033[0m"
        print(message, file=sys.stdout)

    def get_action(self, request):
        if request.method == 'GET':
            return '\033[92mRetrieve request\033[0m'  # Verde para GET
        elif request.method == 'POST':
            return '\033[94mCreate request\033[0m'  # Azul para POST
        elif request.method == 'PUT':
            return '\033[93mUpdate request\033[0m'  # Amarillo para PUT
        elif request.method == 'DELETE':
            return '\033[91mDelete request\033[0m'  # Rojo para DELETE
        elif request.method == 'PATCH':
            return '\033[95mPatch request\033[0m'  # Magenta para PATCH
        elif request.method == 'HEAD':
            return '\033[96mHead request\033[0m'  # Cyan para HEAD
        elif request.method == 'OPTIONS':
            return '\033[97mOptions request\033[0m'  # Blanco para OPTIONS
        else:
            return '\033[1mUnknown request\033[0m'  # Negrita para métodos desconocidos
        



        
class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario está autenticado utilizando TokenAuthentication de DRF
        auth = request.headers.get('Authorization')
        if auth and auth.startswith('Token '):
            print(f'TokenAuthenticationMiddleware')
            key = auth.split(' ')[1]
            token = Token.objects.filter(key=key).first()
            if token is not None:  # Token válido
                request.user = token.user
                print(f'Token:  {token}')
                print(f'user:  {request.user}, id: ',request.user.id)
            else:  # Token inválido
                request.user = AnonymousUser()
                print(f'El Token: es invalido {token}')
        response = self.get_response(request)
        return response