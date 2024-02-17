from collections import defaultdict
from rest_framework import serializers
from drf import settings
from .models import ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais ,ProfesionalServicio

#Registro de servicios
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ProfesionalServicioRelacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesionalServicio
        fields = '__all__'


#relacionar servicios con profesionales
class ProfesionalServicioSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    professional_images = serializers.SerializerMethodField()
    servicios = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    profesional_nombre = serializers.CharField(source='profesional.user.username', read_only=True)
    id = serializers.IntegerField(source='profesional.id', read_only=True)
    user_id = serializers.IntegerField(source='profesional.user.id', read_only=True)
    bibliografia = serializers.CharField(source='profesional.bibliografia', read_only=True)
    class Meta:
        model = Profesional
        fields = ['id','user_id', 'profesional_nombre', 'image', 'professional_images', 'bibliografia', 'servicios']
        
    def get_servicios(self, obj):
        # Obtiene todos los servicios asociados a un profesional específico
        servicios_data = ProfesionalServicio.objects.filter(profesional=obj.profesional).distinct('servicio')
        servicios = []
        for servicio in servicios_data:
            servicios.append({
                'servicio': servicio.servicio.id,
                'servicio_nombre': servicio.servicio.nombre
            })
        return servicios
    def get_image(self, obj):
        # Aquí debes retornar la URL de la imagen del perfil del profesional asociado al servicio
        if obj.profesional.user.image:
            return obj.profesional.user.image.url
        return None

    def get_professional_images(self, obj):
        # Aquí debes retornar una lista de URLs de las imágenes profesionales asociadas al usuario
        professional_images = []
        for image in obj.profesional.user.professional_images.all():
            professional_images.append(image.image.url)
        return professional_images

# Usuario profesional, registro
class ProfessionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalImage
        fields ='__all__'
        
#Registro de usuarios
class UserSerializer(serializers.ModelSerializer):
    professional_images = ProfessionalImageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'descripcion', 'numero_celular', 'image', 'professional_images']
         
class ProfesionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anidamos el UserSerializer aquí
    professional_images = ProfessionalImageSerializer(many=True, read_only=True)  # Agregamos las imágenes profesionales

    class Meta:
        model = Profesional
        fields = ['id', 'user', 'biografia', 'professional_images']
    def get_professional_images(self, obj):
        professional_images = obj.user.professional_images.all()
        return ProfessionalImageSerializer(professional_images, many=True).data
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        professional = Profesional.objects.create(user=user, **validated_data)
        return professional
    

 
        
class UserProfesionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anidar el UserSerializer aquí

    class Meta:
        model = Profesional
        fields = '__all__'

#ubicacion
class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ['id', 'nombre', 'provincia']


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nombre']


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ['id', 'nombre', 'pais']