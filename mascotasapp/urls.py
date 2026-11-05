from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login-sesion/', views.login_sesion, name='login_sesion'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    
    path('mascotas/', views.listar_mascotas, name='listar_mascotas'), 
    path('crear/', views.crear_mascota, name='crear_mascota'),
    path('editar/<int:id>/', views.editar_mascota, name='editar_mascota'),
    path('eliminar/<int:id>/', views.eliminar_mascota, name='eliminar_mascota'),
    
    # --- RUTAS PARA LA API REST ---
    path('api/mascotas/', views.api_mascotas, name='api_mascotas'),
    path('api/mascotas/<int:id>/', views.api_mascota_detalle, name='api_mascota_detalle'),
]