from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from .models import Mascota
from .forms import MascotaForm

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MascotaSerializer


def inicio(request):
    return render(request, 'mascotasapp/login.html')


def login_sesion(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    
    if not username or not password:
        return JsonResponse({'error': 'Completa usuario y contraseña'}, status=400)
    
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Usuario o contraseña incorrectos'}, status=401)
    
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key})


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


@login_required(login_url='inicio')
def listar_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotasapp/inicio.html', {'mascotas': mascotas})


@login_required(login_url='inicio')
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'mascotasapp/crear.html', {'form': form})


@login_required(login_url='inicio')
def editar_mascota(request, id):
    mascotas = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascotas)
        if form.is_valid():
            form.save()
            return redirect('listar_mascotas')
    else:
        form = MascotaForm(instance=mascotas)
    return render(request, 'mascotasapp/editar.html', {'form': form})


@login_required(login_url='inicio')
def eliminar_mascota(request, id):
    mascotas = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        mascotas.delete()
        return redirect('listar_mascotas')
    return render(request, 'mascotasapp/eliminar.html', {'mascota': mascotas})


# --- API REST PROTEGIDA POR TOKEN ---

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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_mascota_detalle(request, id):
    try:
        mascota = Mascota.objects.get(id=id)
    except Mascota.DoesNotExist:
        return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return Response(MascotaSerializer(mascota).data)
    
    elif request.method == 'PUT':
        serializer = MascotaSerializer(mascota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        mascota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)