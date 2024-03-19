from .serializers import ProfesionalServicioRelacionSerializer, ProfessionalImageSerializer, UserSerializer,ServicioSerializer,ProfesionalServicioSerializer,ProfesionalSerializer,UserProfesionalSerializer,CiudadSerializer,ProvinciaSerializer,PaisSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets,permissions
from django.contrib.auth import authenticate, login
from .models import ProfesionalServicio, ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais
from rest_framework.views import APIView
from django.views.generic.edit import FormView
from django.contrib.sessions.models import Session
from django.contrib.auth import login,logout,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from datetime import datetime

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from api.authentication_mixins import Authentication
from api.serializers import UserTokenSerializer
from rest_framework.permissions import AllowAny  # Importa AllowAny
#login
# Create your views here.
#api\views.py
#Login

class UserToken(Authentication, APIView):
    """
    Validate Token
    """
    def get(self,request,*args,**kwargs):        
        try:
            user_token = Token.objects.get(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                'token': user_token.key,
                'user': user.data
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas.'
            },status = status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):
    permission_classes = [AllowAny]
    def post(self,request,*args,**kwargs):
        # send to serializer username and password
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        print('login_serializer: ',login_serializer)
        if login_serializer.is_valid():
            # login serializer return user in validated_data
            user = login_serializer.validated_data['user']
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso.'
                    }, status = status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso.'
                    }, status = status.HTTP_201_CREATED)
                    """
                    return Response({
                        'error': 'Ya se ha iniciado sesión con este usuario.'
                    }, status = status.HTTP_409_CONFLICT)
                    """
            else:
                return Response({'error':'Este usuario no puede iniciar sesión.'}, 
                                    status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos.'},
                                    status = status.HTTP_400_BAD_REQUEST)

    
class Logout(APIView):

    def get(self,request,*args,**kwargs):
        try:
            auth = request.headers.get('Authorization')
            if auth and auth.startswith('Token '):
                print('Valor de "auth": ',auth)
                key = auth.split(' ')[1]
            
                token = Token.objects.filter(key=key).first()
                print('Valor de "token.user": ',token.user)

            if token:
                user = token.user
                # delete all sessions for user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        # search auth_user_id, this field is primary_key's user on the session
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                # delete user token
                token.delete()
                
                session_message = 'Sesiones de usuario eliminadas.'  
                token_message = 'Token eliminado.'
                return Response({'token_message': token_message,'session_message':session_message},
                                    status = status.HTTP_200_OK)
            
            return Response({'error':'No se ha encontrado un usuario con estas credenciales.'},
                    status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se ha encontrado token en la petición.'}, 
                                    status = status.HTTP_409_CONFLICT)


class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        prueba = request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)  # Usa request.data en lugar de request.body
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class UserProfesionalViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny] #Quitar luego en produccion
    queryset = Profesional.objects.all()
    serializer_class = UserProfesionalSerializer

class ProfesionalViewSet(viewsets.ModelViewSet):

    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer

class ServicioViewSet(viewsets.ModelViewSet):  
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ProfesionalServicioRelacionViewSet(viewsets.ModelViewSet):  
    queryset = ProfesionalServicio.objects.all()
    serializer_class = ProfesionalServicioRelacionSerializer

class ProfesionalServicioViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalServicio.objects.all()
    serializer_class = ProfesionalServicioSerializer



class ProfessionalImageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ProfessionalImage.objects.all()
    serializer_class = ProfessionalImageSerializer

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
