from rest_framework import viewsets
from .serializer import UserSerializer,ServicioSerializer,ProfesionalServicioSerializer,ProfesionalSerializer,UserProfesionalSerializer,CiudadSerializer,ProvinciaSerializer,PaisSerializer


from .models import User, Servicio,Profesional,Ciudad,Provincia,Pais

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ServicioViewSet(viewsets.ModelViewSet):  
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ProfesionalServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ProfesionalServicioSerializer 

class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    
class UserProfesionalViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfesionalSerializer
    
class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer