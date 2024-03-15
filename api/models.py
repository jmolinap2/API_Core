from django.db import models
import django.utils.timezone
import uuid
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

#api\models.py



# Extiende el modelo de usuario de Django para agregar campos adicionales

class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(error_messages={'unique': 'Ya existe un usuario con ese nombre de usuario.'},
    help_text='Requerido. 150 caracteres como máximo. Solo letras, dígitos y @/./+/-/_.',
    max_length=150,unique=True,validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],verbose_name='nombre de usuario')
    email = models.EmailField('Correo Electrónico',default=f'@username.com',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    age = models.PositiveIntegerField(null=True, blank=True)
    numero_celular = models.CharField(max_length=15, blank=True, null=True,unique = False)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    date_joined= models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    image = models.ImageField('Imagen de perfil', upload_to='profile_images/', max_length=255, null=True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()


    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name','last_name']

    def __str__(self):
        return f'{self.name} {self.last_name}'
    

# Modelo para las imágenes de perfil de usuario


# Modelo para las imágenes asociadas a un profesional
class ProfessionalImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_images')
    image = models.ImageField(upload_to='professional_images/')

    def __str__(self):
        return f"Imagen de {self.user.username}"
    
    
class Profesional(models.Model):
    user = models.OneToOneField(User, related_name='profesional_data', on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    def get_professional_images(self):
        return ProfessionalImage.objects.filter(user=self.user)
    
#Servicio y ServicioProfesional
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class ProfesionalServicio(models.Model):
    profesional = models.ForeignKey(Profesional, related_name='servicios', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, related_name='profesionales', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.profesional} - {self.servicio}"


#Pais/Provicia/ciudad
    
    
class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
