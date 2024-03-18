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
        #print('headers que llegan a RequestLoggingMiddleware: ', request.headers)
        # Obtenemos la dirección IP del cliente
        ip_address = request.META.get('REMOTE_ADDR', '')
        ip_Origin = request.headers.get('Origin')
        # Si hay un usuario autenticado, lo obtenemos
        user = request.user if request.user.is_authenticated else None
        full_path = request.build_absolute_uri()
        # Imprimimos la información en color
        if user !=None:
            print(f"\033[92mRequest from {ip_address,' ',ip_Origin}, User: {user}, Path: {full_path}\033[0m", file=sys.stdout)
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
                print(f'request.headers: ',request.headers)
                key = auth.split(' ')[1]
                token = Token.objects.get(key=key)
                request.user = token.user
                print(f'Token:  {token}')
                print(f'user:  {request.user}')
            except Token.DoesNotExist:
                request.user = request.user
                # Leer el cuerpo de la solicitud PUT si es necesario
        if request.method == 'PUT':
            # Leer datos del formulario si es multipart/form-data
            if 'multipart/form-data' in request.headers.get('Content-Type', ''):
                # Acceder a los datos del formulario y archivos
                form_data = request.POST
                body = request.body
                files_data = request.FILES

            # Leer datos de JSON si es application/json
            elif 'application/json' in request.headers.get('Content-Type', ''):
                json_data = request.data
                print('Datos JSON:', json_data)
        response = self.get_response(request)
        return response