from .serializers import LoginSerializer, ProfesionalServicioRelacionSerializer, ProfessionalImageSerializer, UserSerializer,ServicioSerializer,ProfesionalServicioSerializer,ProfesionalSerializer,UserProfesionalSerializer,CiudadSerializer,ProvinciaSerializer,PaisSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.contrib.auth import authenticate, login
from .models import ProfesionalServicio, ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais
from rest_framework.views import APIView
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Importa AllowAny
import json
#login
# Create your views here.
#api\views.py
#Login 
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Verificar si el usuario ya está autenticado
        if request.user.is_authenticated:
            user = request.user
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            user_data['token'] = token.key

            if created:
                return Response({"user": user_data, "detail": "Token creado exitosamente."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"user": user_data, "detail": "Usuario ya estaba logueado."}, status=status.HTTP_200_OK)

        # Verificar las credenciales del usuario
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Obtener o crear el token del usuario
            token, created = Token.objects.get_or_create(user=user)

            # Serializar los datos del usuario y crear la respuesta
            user_data = UserSerializer(user).data
            user_data['token'] = token.key

            if created:
                return Response({"user": user_data, "detail": "Token creado exitosamente."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"user": user_data, "detail": "Usuario ya estaba logueado."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    def post(self, request, format=None):
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            # Obtener el token de autenticación del usuario desde los encabezados de autorización
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Token '):
                provided_token = auth_header.split(' ')[1]
                # Verificar si el token proporcionado coincide con el token del usuario
                if provided_token == request.user.auth_token.key:
                    # Eliminar el token de autenticación del usuario
                    request.user.auth_token.delete()
                    return Response({"detail": "Usuario deslogueado exitosamente."}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Token de autenticación inválido."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Encabezado de autorización no válido."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "No hay usuario autenticado."}, status=status.HTTP_400_BAD_REQUEST)
       
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class ServicioViewSet(viewsets.ModelViewSet):  
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ProfesionalServicioRelacionViewSet(viewsets.ModelViewSet):  
    queryset = ProfesionalServicio.objects.all()
    serializer_class = ProfesionalServicioRelacionSerializer

class ProfesionalServicioViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalServicio.objects.all()
    serializer_class = ProfesionalServicioSerializer

class ProfesionalViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] #Quitar luego en produccion
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer

class ProfessionalImageViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalImage.objects.all()
    serializer_class = ProfessionalImageSerializer
    
class UserProfesionalViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(profesional_data__isnull=False)  # Filtra solo los usuarios que tienen datos de profesional
    serializer_class = UserProfesionalSerializer

class UserProfesionaloNoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Tieneno o no datos de profesional
    serializer_class = UserProfesionalSerializer


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

# Obtén todos los miembros del módulo actual
members = vars()

# Filtra las clases que son subclases de viewsets.ModelViewSet
viewsets_list = [members[name] for name in members if isinstance(members[name], type) and issubclass(members[name], viewsets.ModelViewSet)]
