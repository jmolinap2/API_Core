from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Persona(models.Model):
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    # Agregar campos opcionales para vendedor

    correo = models.EmailField(blank=True, null=True)
    numero_celular = models.CharField(max_length=15, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.fullname} (ID: {self.id})"
    
    
class Profesional(models.Model):
    persona = models.OneToOneField(Persona, related_name='profesional', on_delete=models.CASCADE)
    biografia = models.TextField(blank=True)
    imagen_perfil = models.ImageField(upload_to='imagenes/', blank=True, null=True)

    def __str__(self):
        return self.persona.fullname


class Imagen(models.Model):
    persona = models.ForeignKey(Persona, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/')
    
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