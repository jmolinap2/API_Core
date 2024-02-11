from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'personas', views.PersonaViewSet)  # Registro de la vista para personas
router.register(r'imagenes', views.ImagenViewSet)  # Registro de la nueva vista para imágenes
router.register(r'profesional', views.ProfesionalViewSet)

urlpatterns = [
    path('', include(router.urls))
]
