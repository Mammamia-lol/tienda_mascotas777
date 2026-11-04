from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota
from .forms import MascotaForm

# Importaciones para la API y la seguridad por Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MascotaSerializer

# Vista principal ahora carga el Login profesional
def inicio(request):
    return render(request, 'mascotasapp/login.html')

# Vista para Leer (Read) - El inventario de la tienda
def listar_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotasapp/inicio.html', {'mascotas': mascotas})

# Vista para Crear (Create)
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'mascotasapp/crear.html', {'form': form})

# Vista para Actualizar (Update)
def editar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'mascotasapp/editar.html', {'form': form})

# Vista para Eliminar (Delete)
def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        mascota.delete()
        return redirect('listar_mascotas')
    return render(request, 'mascotasapp/eliminar.html', {'mascota': mascota})

# --- VISTA DE LA API PROTEGIDA POR TOKEN ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_mascotas(request):
    if request.method == 'GET':
        mascotas = Mascota.objects.all()
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)