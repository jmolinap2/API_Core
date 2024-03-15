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
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')
        
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields ='__all__'
        read_only_fields = ('date_joined','last_login')

    def create(self, validated_data):
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data, password=password)
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data:
            instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        if 'groups' in validated_data:
            groups = validated_data.pop('groups')
            instance.groups.set(groups)

        if 'user_permissions' in validated_data:
            user_permissions = validated_data.pop('user_permissions')
            instance.user_permissions.set(user_permissions)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self,instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }
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
        
        email = user_data.pop('email', None)
        name = user_data.pop('name', None)
        last_name = user_data.pop('last_name', None)
        numero_celular = user_data.pop('numero_celular', None)
        username = user_data.pop('username', None)
        user = User(username=username,
                    email=email, name=name,
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