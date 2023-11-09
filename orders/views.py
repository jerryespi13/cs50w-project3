from django.apps import apps
from django.contrib.auth import authenticate
# para no tener conflicto con la vista logout (por el nombre)
from django.contrib.auth import logout as logout_auth
# para no tener conflicto con la vista login (por el nombre)
from django.contrib.auth import login as login_auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
# para mensajes 
from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()

totalOrden = 0

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

    else:
        return render(request, "orders/login.html")
    
def logout(request):
    logout_auth(request)
    return JsonResponse("login", safe=False)

# cambiar precio en pantalla
def change_Price(request):
    if request.method == 'POST':
        # obtenemos los datos
        datos = json.loads(request.body)

        # obtenemos el precio del producto
        precioProducto = calcular_precio(datos)

        return JsonResponse(precioProducto, safe=False)
    else:
        return JsonResponse({"mensaje": "Método no permitido"}, status=405)
    

def calcular_precio(datos):
        app_name = 'orders'
        # Obtienemos los modelos de la aplicación
        app_models = apps.get_app_config(app_name).get_models()
        # Extraemos los nombres de las tablas de la base de datos de los modelos
        # A las tablas donde guardo los productos les puse el mismo nombre de la class
        table_names = [model._meta.db_table for model in app_models]

        nombreModelo = ""
        priceElementSelect = 0
        precioExtra = 0
        nuevoPrecioProducto = 0
        for table_name in table_names:
            if not table_name.__contains__("orders_"):
                nombreModelo = table_name
                Modelo = apps.get_model(app_name, nombreModelo)

                # buscamos el elemento en cada tabla
                try:
                    # obtenemos la instancia del producto al que se le dio click
                    producto = Modelo.objects.get(id=datos["idElement"], name=datos["nombreElement"])
                    # para los productos que no tienen size, que solo tinenen un precio: pasta y Salads
                    if not datos["sizeElement"]:
                        priceElementSelect = producto.price
                        return priceElementSelect

                    # si el tamaño seleccionado es Small
                    if datos["sizeElement"] == "Small":
                        priceElementSelect = producto.small_price

                        # si viene uno o mas extras seleccionados
                        if datos["nombreExtra"]:
                            # sumamos el precio de cada extra
                            for _ in range(datos["numerosExtras"]):
                                for extra in producto.extras.all():
                                    if datos["nombreExtra"] == extra.name:
                                        precioExtra += extra.price
                            # y al precio del elemento se le suma el precio de los extras totales
                            nuevoPrecioProducto = priceElementSelect + precioExtra

                            # retornamos el precio del elemento mas el total de los extras
                            return nuevoPrecioProducto

                     # si el tamaño seleccionado es Large
                    elif datos["sizeElement"] == "Large":
                        priceElementSelect = producto.large_price

                         # si viene uno o mas extras seleccionados
                        if datos["nombreExtra"]:
                            # sumamos el precio de cada extra
                            for _ in range(datos["numerosExtras"]):
                                for extra in producto.extras.all():
                                    if datos["nombreExtra"] == extra.name:
                                        precioExtra += extra.price
                            # y al precio del elemento se le suma el precio de los extras totales
                            nuevoPrecioProducto = priceElementSelect + precioExtra

                            # retornamos el precio del producto mas el precio de los extras
                            return nuevoPrecioProducto

                except:
                    nombreModelo = ""
                    continue
        
        # si no hay extra selecionado sea por que no se seleciono o no tiene
        # se devuelve el precio tipo de tamaño de ese producto
        return priceElementSelect

def cart(request):
    """Cart
    
        Filtrado de datos antes de añadir al cart

    """
    
    if request.method == "POST":
        # obtenemos los datos
        datos = json.loads(request.body)
        app_name = 'orders'
        # Obtienemos los modelos de la aplicación
        app_models = apps.get_app_config(app_name).get_models()
        # Extraemos los nombres de las tablas de la base de datos de los modelos
        # A las tablas donde guardo los productos les puse el mismo nombre de la class
        table_names = [model._meta.db_table for model in app_models]

        nombreModelo = ""
        priceElementSelect = 0
        precioExtra = 0
        nuevoPrecioProducto = 0
        for table_name in table_names:
            if not table_name.__contains__("orders_"):
                nombreModelo = table_name
                Modelo = apps.get_model(app_name, nombreModelo)

                # buscamos el elemento en cada tabla
                try:
                    # obtenemos la instancia del producto al que se le dio click
                    producto = Modelo.objects.get(id=datos["idElement"], name=datos["nombreElement"])

                    if datos["sizeElement"] == "":
                        priceElementSelect = producto.price
                        return JsonResponse(priceElementSelect, safe=False)

                    # si el tamaño seleccionado es Small
                    elif datos["sizeElement"] == "Small":
                        priceElementSelect = producto.small_price

                        # si viene uno o mas extras seleccionados
                        if datos["extrasSelected"]:
                            print("extra")
                            # sumamos el precio de cada extra
                            for i in range(len(datos["extrasSelected"])):
                                for extra in producto.extras.all():
                                    if datos["extrasSelected"][i] == extra.name:
                                        precioExtra += extra.price
                            # y al precio del elemento se le suma el precio de los extras totales
                            nuevoPrecioProducto = priceElementSelect + precioExtra

                            # retornamos el precio del elemento mas el total de los extras
                            return JsonResponse(nuevoPrecioProducto, safe=False)

                     # si el tamaño seleccionado es Large
                    elif datos["sizeElement"] == "Large":
                        priceElementSelect = producto.large_price

                         # si viene uno o mas extras seleccionados
                        if datos["extrasSelected"]:
                            # sumamos el precio de cada extra
                            for i in range(len(datos["extrasSelected"])):
                                for extra in producto.extras.all():
                                    if datos["extrasSelected"][i] == extra.name:
                                        precioExtra += extra.price
                            # y al precio del elemento se le suma el precio de los extras totales
                            nuevoPrecioProducto = priceElementSelect + precioExtra

                            # retornamos el precio del producto mas el precio de los extras
                            return JsonResponse(nuevoPrecioProducto, safe=False)
                except:
                    nombreModelo = ""
                    continue
        
        return JsonResponse(priceElementSelect, safe=False)
    else:
        return JsonResponse({"mensaje": "Método no permitido"}, status=405)

def realizar_pedido(request):
    if request.method == "POST":
        print("aqui andamos")
        # obtenemos los datos
        totalCart = 0
        datos = json.loads(request.body) 
        # el usuario siempre viene de ultimo en la variable datos
        usuario = datos[-1]
        print(usuario)
        print(len(datos[0]))
        
        for i in range(len(datos[0])):
            print(datos[0][i])
            # calculamos el precio de cada producto multiplicado por su cantidad
            precio = calcular_precio(datos[0][i]) * datos[0][i]["cantidad"]
            # el precio de cada producto se va sumanando al total
            totalCart += precio
            print(precio)
            print("-------------------------------------------------------")
        print(totalCart)

        return JsonResponse({"mensaje":"llego"})