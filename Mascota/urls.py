from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views # <-- Importamos la herramienta de tokens

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mascotasapp.urls')), # Aquí viven tus HTML de la Eva 2
    
    # Nueva ruta de la API para que tu Login solicite el Token de acceso:
    path('api/token/', authtoken_views.obtain_auth_token, name='api_token_auth'),
]