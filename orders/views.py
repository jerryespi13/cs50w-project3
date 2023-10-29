from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def register(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        usuario = request.POST["usuario"]
        contraseña = request.POST["contraseña"]
        confirmacion = request.POST["confirmarContraseña"]
        direccion = request.POST["direccion"]
        telefono = request.POST["telefono"]
       

        print(nombre + apellido + usuario + contraseña + confirmacion + direccion + telefono)
        return render(request, "orders/register.html")

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
