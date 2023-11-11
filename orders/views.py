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
from django.contrib.auth.decorators import login_required

# no se porque en los celulares me da problema el csrf_token
# con esto me salto ese problema
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
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
                        #return priceElementSelect

                    # si el tamaño seleccionado es Small
                    if datos["sizeElement"] == "Small":
                        priceElementSelect = producto.small_price

                        # si viene uno o mas extras seleccionados
                        if datos["extrasSelected"]:
                            # sumamos el precio de cada extra
                            for i in range(len(datos["extrasSelected"])):
                                for extra in producto.extras.all():
                                    if datos["extrasSelected"][i] == extra.name:
                                        precioExtra += extra.price
                            # y al precio del elemento se le suma el precio de los extras totales
                            nuevoPrecioProducto = priceElementSelect + precioExtra
                            # retornamos el precio del elemento mas el total de los extras
                            return nuevoPrecioProducto

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
                            return nuevoPrecioProducto

                except:
                    nombreModelo = ""
                    continue
        
        # si no hay extra selecionado sea por que no se seleciono o no tiene
        # se devuelve el precio tipo de tamaño de ese producto
        return priceElementSelect

@csrf_exempt
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
    
@csrf_exempt
def realizar_pedido(request):
    if request.method == "POST":
        extras = []
        toppings = []
        size = ""
        nombre =""
        cantidad = 0
        priceElement = 0
        # obtenemos los datos
        totalCart = 0
        datos = json.loads(request.body) 
        # el usuario siempre viene de ultimo en la variable datos
        usuario = datos[-1]

        #creamos la instancia de la orden
        usuario_orden = User.objects.get(username=usuario)
        nueva_orden = Orden(usuario=usuario_orden)
        nueva_orden.save()

        for i in range(len(datos[0])):
            nombre = datos[0][i]["nombreElement"]
            cantidad = datos[0][i]["cantidad"]
            size = datos[0][i]["sizeElement"]
            tamaño = Tamaño.objects.get(nombre=size) if size else None
            if "toppingsSelected" in datos[0][i] and datos[0][i]["toppingsSelected"]:
                toppings = Topping.objects.filter(nombre__in= datos[0][i]["toppingsSelected"])
            if "extrasSelected" in datos[0][i] and datos[0][i]["extrasSelected"]:
                extras = extras = Extra.objects.filter(name__in=datos[0][i]["extrasSelected"])

            # calculamos el precio de cada producto multiplicado por su cantidad
            priceElement = calcular_precio(datos[0][i])
            precio = priceElement * datos[0][i]["cantidad"]
            # el precio de cada producto se va sumanando al total
            totalCart += precio
            # Crea una nueva instancia de OrdenProducto para cada producto
            producto_orden = OrdenProducto(orden=nueva_orden, cantidad=cantidad, name=nombre, size=tamaño, price=priceElement)
            # Agrega extras y toppings al producto
            producto_orden.save()
            producto_orden.extras.set(extras)
            producto_orden.toppings.set(toppings)
            producto_orden.save()
            extras = []
            toppings = []
        nueva_orden.total = totalCart
        nueva_orden.save()
        

        return JsonResponse({"mensaje":"llego"})

@login_required
def usuario_view(request):
    context = {
        "user": User.objects.get(username=request.user),
        "orders": Orden.objects.filter(usuario=request.user)
    }
    return render(request, "orders/user.html", context) 

def eliminarPedido(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        ordenEliminar = Orden.objects.get(pk=order_id)
        ordenEliminar.delete()
        return redirect(to = "usuario_view")
    
def verOrden(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        context = {
        "user": User.objects.get(username=request.user),
        "orden":  Orden.objects.get(id=order_id)
    }
        return render(request, "orders/verOrden.html", context)