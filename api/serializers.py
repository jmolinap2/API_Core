from asyncio import exceptions
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from drf import settings
from django.contrib.auth import get_user_model
from .models import ProfessionalImage, User, Servicio,Profesional,Ciudad,Provincia,Pais ,ProfesionalServicio
from rest_framework.exceptions import ValidationError
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
    class Meta:
        model = ProfesionalServicio
        fields = '__all__'
#Login
        

#api\serializers.py
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Este usuario está desactivado.")

                return user
            else:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Se requiere un nombre de usuario y contraseña.")

# Usuario profesional, registro
class ProfessionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalImage
        fields = ('id', 'image', 'user')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Obtenemos la URL completa de la imagen
        image_url = instance.image.url if instance.image else None
        representation['image'] = self.context['request'].build_absolute_uri(image_url)
        return representation
        
#Registro de usuarios
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('date_joined', 'last_login')

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        user = super().create(validated_data)
        self._update_user(user, validated_data, groups_data)
        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        user = super().update(instance, validated_data)
        self._update_user(user, validated_data, groups_data)
        return user

    def _update_user(self, user, validated_data, groups_data):
        password = validated_data.get('password')
        if password:
            user.set_password(password)
        user.save()
        if groups_data is not None:
            try:
                user.groups.set(groups_data)
            except exceptions.ObjectDoesNotExist:
                # Manejar cualquier excepción potencial aquí
                ...
        
         
class UserProfesionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Anidamos el UserSerializer aquí
    professional_images = serializers.SerializerMethodField()
    class Meta:
        model = Profesional
        fields = '__all__'
    def get_professional_images(self, obj):
        # Obtenemos las imágenes profesionales asociadas al profesional actual
        professional_images = ProfessionalImage.objects.filter(user=obj.user)
        # Serializamos las imágenes profesionales y retornamos los datos
        serializer = ProfessionalImageSerializer(professional_images, many=True, context=self.context)
        return serializer.data
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.get('password', None)
        age = user_data.pop('age', None)
        descripcion = user_data.pop('descripcion', None)
        email = user_data.pop('email', None)
        first_name = user_data.pop('first_name', None)
        last_name = user_data.pop('last_name', None)
        numero_celular = user_data.pop('numero_celular', None)
        username = user_data.pop('username', None)
        user = User(username=username, descripcion=descripcion,
                    email=email, first_name=first_name,
                    last_name=last_name, age=age,
                    numero_celular=numero_celular)  # no debo poner lo demas datos de user?
        user.save()  # no, eso es por default
        user.set_password(password)
        user.save()  # como se hace para entrar en este modo? eso de debuguear f8, como pongo siguiente paso?

        # Obtener datos de grupos y manejar posibles errores
        groups_data = validated_data.pop('groups', None)
        if groups_data:
            try:
                # Usa groups.set() para asignar grupos correctamente
                user.groups.set(groups_data)
            except exceptions.ObjectDoesNotExist:
                # Maneja cualquier excepción potencial aquí, p.ej., registra o devuelve una respuesta de error
                ...

        #user = User.objects.create_user(**user, password=password)
        professional = Profesional.objects.create(user=user, **validated_data)
        return professional

class ProfesionalSerializer(serializers.ModelSerializer):

    professional_images = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    class Meta:
        model = Profesional
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.user.username  # Agregar el nombre de usuario a la representación
        return representation
    def get_professional_images(self, obj):
        # Obtenemos las imágenes profesionales asociadas al profesional actual
        professional_images = ProfessionalImage.objects.filter(user=obj.user)
        # Serializamos las imágenes profesionales y retornamos los datos
        serializer = ProfessionalImageSerializer(professional_images, many=True, context=self.context)
        return serializer.data
    def get_user_image(self, obj):  # Método para obtener la imagen del usuario
        if obj.user.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.image.url)
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