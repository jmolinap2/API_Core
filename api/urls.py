from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'User', views.UserViewSet) # Registro de la vista para User
#router.register(r'Servicio', views.ServicioViewSet)

router.register(r'Profesional', views.ProfesionalViewSet)
router.register(r'User-Profesional', views.UserProfesionalViewSet)  # Registro de la vista personalizada
router.register(r'Profesional-Servicio', views.ProfesionalServicioViewSet)

router.register(r'Ciudad', views.CiudadViewSet)
router.register(r'Pais', views.PaisViewSet)
router.register(r'Provincia', views.ProvinciaViewSet)
router.register(r'Servicio', views.ServicioViewSet)


urlpatterns = [
    path('', include(router.urls))
]
