from django.utils.deprecation import MiddlewareMixin
import sys
class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtenemos la dirección IP del cliente
        ip_address = request.META.get('REMOTE_ADDR', '')
        # Si hay un usuario autenticado, lo obtenemos
        user = request.user if request.user.is_authenticated else None
        full_path = request.build_absolute_uri()
        # Imprimimos la información en color
        if user:
            print(f"\033[92mRequest from {ip_address}, User: {user}, Path: {full_path}\033[0m", file=sys.stdout)
        else:
            print(f"\033[91mRequest from {ip_address}, User: anonymous, Path: {full_path}\033[0m", file=sys.stdout)
