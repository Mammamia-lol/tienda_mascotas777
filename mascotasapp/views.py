from django.shortcuts import render
from .models import Mascota

def inicio(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotasapp/inicio.html', {'mascotas': mascotas})