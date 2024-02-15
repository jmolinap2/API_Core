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
        model = Servicio
        fields = '__all__'

#Registro de usuarios
class UserSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(source='image', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'descripcion', 'numero_celular', 'image']

#relacionar servicios con profesionales
class ProfesionalServicioSerializer(serializers.ModelSerializer):
    profesional_nombre = serializers.CharField(source='profesional.user.username', read_only=True)
    servicios = serializers.SerializerMethodField()

    class Meta:
        model = ProfesionalServicio
        fields = ['profesional', 'profesional_nombre', 'servicios']

    def get_servicios(self, obj):
        servicios_data = obj.profesional.servicios.all()
        servicios = []
        for servicio in servicios_data:
            servicios.append({
                'servicio': servicio.id,
                'servicio_nombre': servicio.nombre
            })
        return servicios

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {
            'profesional': ret['profesional'],
            'profesional_nombre': ret['profesional_nombre'],
            'servicios': ret['servicios']
        }

# Usuario profesional, registro
class ProfessionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalImage
        fields = ['image']
        
class ProfesionalSerializer(serializers.ModelSerializer):
    user_image_url = serializers.SerializerMethodField()
    servicios = serializers.PrimaryKeyRelatedField(many=True, queryset=Servicio.objects.all())

    class Meta:
        model = Profesional
        fields = ['id', 'user', 'biografia', 'user_image_url', 'servicios']

    def get_user_image_url(self, obj):
        if obj.user.image:
            return self.context['request'].build_absolute_uri(obj.user.image.url)
        else:
            # Construye la URL para la imagen empty.png
            relative_url = 'static/img/empty.png'
            return self.context['request'].build_absolute_uri(relative_url)
        
class UserProfesionalSerializer(serializers.ModelSerializer):
    professional_images = ProfessionalImageSerializer(many=True, read_only=True)
    servicios = ServicioSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age',
                  'descripcion', 'numero_celular', 'image', 'professional_images',
                  'profesional_data', 'servicios']

    profesional_data = serializers.SerializerMethodField()

    def get_profesional_data(self, obj):
        try:
            profesional = Profesional.objects.get(user=obj)
            return {'biografia': profesional.biografia}
        except Profesional.DoesNotExist:
            return None

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