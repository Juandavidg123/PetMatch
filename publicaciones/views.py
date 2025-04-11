from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all().order_by('-creado_en')
    return render(request, 'lista.html', {'publicaciones': publicaciones})

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            messages.success(request, '¡Publicación creada!')
            return redirect('lista_publicaciones')
    else:
        form = PublicacionForm()
    return render(request, 'formulario.html', {'form': form})

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if publicacion.autor != request.user:
        messages.error(request, 'No puedes editar esta publicación.')
        return redirect('lista_publicaciones')

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Publicación actualizada!')
            return redirect('lista_publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'formulario.html', {'form': form})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if publicacion.autor == request.user:
        publicacion.delete()
        messages.success(request, 'Publicación eliminada.')
    else:
        messages.error(request, 'No puedes eliminar esta publicación.')
    return redirect('lista_publicaciones')

def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'detalle.html', {'publicacion': publicacion})
