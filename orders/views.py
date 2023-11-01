from django.contrib.auth import authenticate, logout
# para no tener conflicto con la vista login (por el nombre)
from django.contrib.auth import login as login_auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
# para mensajes tipo alert
from django.contrib import messages

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

        if usuario == "":
            messages.info(request, 'Ingresa usuario')
            return render(request, "orders/register.html")

        elif contraseña == "" or confirmacion == "":
            messages.info(request, 'Ingresa campo contraseña')
            return render(request, "orders/register.html")
        
        elif contraseña != confirmacion:
            messages.info(request, 'contraseñas deben de ser iguales')
            return render(request, "orders/register.html")

        if contraseña == confirmacion:
            print("contraseñas iguales")
            if User.objects.filter(username=usuario).exists():
                messages.info(request, "Usuario ya existe")
                return render(request, 'orders/register.html')
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
                messages.info(request, "Usuario creado, inicie sesión")
                return redirect(to = "login")

    else:
        return render(request, "orders/register.html")

def login(request):
    if request.method == "POST":
        usuario = request.POST["usuario"]
        contraseña = request.POST["contraseña"]
        if usuario == "" or contraseña == "":
            messages.info(request, "Ingrese los datos solicitados")
            return render(request, 'orders/login.html')
        
        user = authenticate(username = usuario, password = contraseña)
        if user is not None:
            login_auth(request, user)
            return redirect (to = "index")
        else:
            messages.success(request, 'Usuario o contraseña incorrecta.')
            return redirect(to='login')


        return render(request, "orders/login.html")

    else:
        return render(request, "orders/login.html")
    
def logout(request):
    return render(request, "orders/login.html", {"message": "Logged out."})