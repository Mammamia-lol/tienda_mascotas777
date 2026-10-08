from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota
from .forms import MascotaForm

# Vista principal
def inicio(request):
    return render(request, 'mascotasapp/inicio.html')

# Vista para Leer (Read) - El inventario
def listar_mascotas(request):
    mascotas = Mascota.objects.all()
    # Enviamos los datos a inicio.html, ya que ahí pusiste la tabla del inventario
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