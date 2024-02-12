from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'User', views.UserViewSet)  # Registro de la vista para User

router.register(r'Profesional', views.ProfesionalViewSet)
router.register(r'User-Profesional', views.UserProfesionalViewSet)  # Registro de la vista personalizada

urlpatterns = [
    path('', include(router.urls))
    #,path('user-profesional2/', views.CreateUserProfesionalViewSet.as_view(), name='user-profesional')
]
