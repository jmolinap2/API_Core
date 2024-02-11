from rest_framework import viewsets
from .models import Persona, Imagen , Profesional # Importa el modelo de Imagen
from .serializer import PersonaSerializer, ImagenSerializer , ProfesionalSerializer  # Importa el serializador de Imagen

# Create your views here.


class PersonaViewSet(viewsets.ModelViewSet):  # Cambia el nombre de la vista
    queryset = Persona.objects.all()  # Cambia el nombre del modelo
    serializer_class = PersonaSerializer  # Cambia el nombre del serializador

class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    
class ImagenViewSet(viewsets.ModelViewSet):  # Define una nueva clase de vista para las imágenes
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer