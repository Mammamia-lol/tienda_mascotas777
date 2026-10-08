from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mascotas/', views.listar_mascotas, name='listar_mascotas'), 
    path('crear/', views.crear_mascota, name='crear_mascota'),
    path('editar/<int:id>/', views.editar_mascota, name='editar_mascota'),
    path('eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),
]