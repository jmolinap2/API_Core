from rest_framework import serializers
from .models import Persona, Imagen, Profesional

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    imagenes = ImagenSerializer(many=True, read_only=True)  # Asumiendo que cada persona puede tener varias imágenes

    class Meta:
        model = Persona
        fields = '__all__'
        
class ProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesional
        fields = '__all__'