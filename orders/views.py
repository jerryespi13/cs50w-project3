from django.contrib.auth import authenticate
# para no tener conflicto con la vista logout (por el nombre)
from django.contrib.auth import logout as logout_auth
# para no tener conflicto con la vista login (por el nombre)
from django.contrib.auth import login as login_auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
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
        "pastas": Pasta.objects.all(),
        "salads": Salads.objects.all(),
        "dinners": DinnerPlate.objects.all(),
        "subs": Sub.objects.all(),
        "pizzas": Pizza.objects.all(),
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

        # validamos ciertos inputs
        if usuario == "":
            messages.info(request, 'Ingresa usuario')
            return render(request, "orders/register.html")

        elif contraseña == "" or confirmacion == "":
            messages.info(request, 'Ingresa campo contraseña')
            return render(request, "orders/register.html")
        
        elif contraseña != confirmacion:
            messages.info(request, 'contraseñas deben de ser iguales')
            return render(request, "orders/register.html")

        elif contraseña == confirmacion:
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
    logout_auth(request)
    return render(request, "orders/login.html")

def extras(request):
    if request.method == 'POST':
        # obtenemos los datos
        datos = json.loads(request.body)

        # algunas variables para hacer calculos
        producto = Sub.objects.get(pk=datos["idElement"])

        # obtenemos el precio del producto
        precioProducto = 0
        sizeProducto = datos["sizeElement"]
        if sizeProducto == "Small":
            precioProducto = producto.small_price
        elif sizeProducto == "Large":
            precioProducto = producto.large_price
        
        # obtenemos el numero de extras seleccionados
        numerosExtras = datos["numerosExtras"]
        
        # obtenemos el precio total de los extra
        precioExtra = 0
        nombreExtra = datos["nombreExtra"]
        for _ in range(numerosExtras):
            for extra in producto.extras.all():
                if nombreExtra == extra.name:
                    precioExtra += extra.price
        nuevoPrecioProducto = precioProducto + precioExtra

        # retornamos el calculo obtenido
        return JsonResponse(nuevoPrecioProducto, safe=False)
    else:
        return JsonResponse({"mensaje": "Método no permitido"}, status=405)