from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
def index(request):
    context = {
        "user": request.user
    }
    return render(request, "orders/index.html", context)

#registro de un usuario
def register(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        usuario = request.POST["usuario"]
        contraseña = request.POST["contraseña"]
        confirmacion = request.POST["confirmarContraseña"]
        direccion = request.POST["direccion"]
        telefono = request.POST["telefono"]

        if contraseña == confirmacion:
            print("contraseñas iguales")
            if User.objects.filter(username=usuario).exists():
                return render(request, 'orders/register.html', {"message": "Usuario Ya existe."})
            else:
                user = User.objects.create_user(
                                                first_name=nombre,
                                                last_name=apellido,
                                                username=usuario,
                                                password=contraseña,
                                                phone=telefono,
                                                location=direccion
                    )
                user.save()
                return render(request, 'orders/login.html',{"message": "Usuario Creado, inicia sesión."})

    else:
        return render(request, "orders/register.html")

def login(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        contraseña = request.POST["contraseña"]
        print(usuario + contraseña)
        return render(request, "orders/login.html")

    else:
        return render(request, "orders/login.html")
    
def logout(request):
    return render(request, "orders/login.html", {"message": "Logged out."})