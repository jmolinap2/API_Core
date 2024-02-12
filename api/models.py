from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# Extiende el modelo de usuario de Django para agregar campos adicionales
class User(AbstractUser): 
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name='Imagen')
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    numero_celular = models.CharField(max_length=15, blank=True, null=True)
    #groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    #user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    

    def __str__(self):
        return self.username

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
    
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

    
class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre