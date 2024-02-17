from rest_framework import viewsets
from .serializer import ProfesionalServicioRelacionSerializer, ProfessionalImageSerializer, UserSerializer,ServicioSerializer,ProfesionalServicioSerializer,ProfesionalSerializer,UserProfesionalSerializer,CiudadSerializer,ProvinciaSerializer,PaisSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import ProfesionalServicio, ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais

# Create your views here.


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
