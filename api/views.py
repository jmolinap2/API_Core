from rest_framework import viewsets
from .models import User , Profesional # Importa el modelo de Imagen
from .serializer import UserSerializer, ProfesionalSerializer ,UserProfesionalSerializer # Importa el serializador de Imagen
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Profesional

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):  # Cambia el nombre de la vista
    queryset = User.objects.all()  # Cambia el nombre del modelo
    serializer_class = UserSerializer  # Cambia el nombre del serializador

class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    
class UserProfesionalViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfesionalSerializer