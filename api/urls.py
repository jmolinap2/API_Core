from django.urls import path, include
from rest_framework import routers
from api import views
from .views import Login, viewsets_list
from api.user.api import user_api_view,user_detail_api_view

router = routers.DefaultRouter()

""" for viewset in viewsets_list:
    # Obtiene el nombre de la clase sin el sufijo "ViewSet" para usar como prefijo en el registro
    prefix = viewset.__name__.replace('ViewSet', '')

    # Registra la vista en el enrutador utilizando el nombre de la clase como prefijo
    router.register(rf'{prefix}', viewset)
router = routers.DefaultRouter() """
# Define tus viewsets
router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')
#router.register(r'usuarios', user_api_view, basename='usuarios')

router.register(r'userprofesionales', views.UserProfesionalViewSet, basename='userprofesionales')
router.register(r'profesionales', views.ProfesionalViewSet, basename='profesionales')


router.register(r'servicios', views.ServicioViewSet, basename='servicios')
router.register(r'profesionalserviciosrelacion', views.ProfesionalServicioRelacionViewSet, basename='profesionalserviciosrelacion') 
router.register(r'profesionalservicios', views.ProfesionalServicioViewSet, basename='profesionalservicios') 
router.register(r'profesionalesImagenes', views.ProfessionalImageViewSet, basename='profesionalesImagenes')


""" router.register(r'paises', views.PaisViewSet)
router.register(r'provincias', views.ProvinciaViewSet)
router.register(r'ciudades', views.CiudadViewSet) """

urlpatterns = [
    path('', include(router.urls)),
    #path('login/', LoginView.as_view(), name='login'),
]

