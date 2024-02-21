from .serializer import LoginSerializer, ProfesionalServicioRelacionSerializer, ProfessionalImageSerializer, UserSerializer,ServicioSerializer,ProfesionalServicioSerializer,ProfesionalSerializer,UserProfesionalSerializer,CiudadSerializer,ProvinciaSerializer,PaisSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.contrib.auth import authenticate, login
from .models import ProfesionalServicio, ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Importa AllowAny
#login
# Create your views here.

#Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            
            # Obtener el token del usuario
            try:
                token = Token.objects.get(user=user)
                user_data = UserSerializer(user).data
                user_data['token'] = token.key
                return Response({"user": user_data}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "El token del usuario no se encontró."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)
       
class UserViewSet(viewsets.ModelViewSet):
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
