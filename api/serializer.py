from rest_framework import serializers

from drf import settings
from .models import User, Profesional, Servicio


        
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(source='image', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'descripcion', 'numero_celular', 'image']
        
class ProfesionalSerializer(serializers.ModelSerializer):
    user_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profesional
        fields = ['id', 'user', 'biografia', 'user_image_url', 'servicios']

    def get_user_image_url(self, obj):
        if obj.user.image:
            return self.context['request'].build_absolute_uri(obj.user.image.url)
        return f"{settings.STATIC_URL}img/empty.png"
        
class UserProfesionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age',
                   'descripcion', 'numero_celular', 'biografia','image', 'servicios']  # Incluye 'biografia' en la lista de campos

    biografia = serializers.CharField(source='profesional_data.biografia', read_only=True)  # Campo de Profesional
    servicios = serializers.CharField(source='profesional_data.servicios', read_only=True)

    def create(self, validated_data):
        user_data = validated_data.pop('profesional_data', {})
        user = User.objects.create(**validated_data)
        Profesional.objects.create(user=user, **user_data)
        return user