from django.contrib import admin
from .models import Persona, Imagen

# Register your models here.

class ImagenInline(admin.TabularInline):  # Opcionalmente puedes usar admin.StackedInline para un diseño diferente
    model = Imagen
    extra = 0  # Esto determina cuántos formularios en línea vacíos se muestran de forma predeterminada

class PersonaAdmin(admin.ModelAdmin):
    inlines = [ImagenInline]

admin.site.register(Persona, PersonaAdmin)
admin.site.register(Imagen)
