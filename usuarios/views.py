from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def registro_view(request):
    try:
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido a PetMatch.')
                return redirect('home')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario.')
        else:
            form = RegistroForm()
    except Exception as e:
        messages.error(request, f'Ocurrió un error inesperado: {str(e)}')
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')
