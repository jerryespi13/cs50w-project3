# Project 3

Web Programming with Python and JavaScript

## Información del proyecto
- Titulo:  `Pizza`
- Autor:  `Jerry Ronaldo Espino Inestroza`
- Descripción: Proyecto 3 de programación web. se trata de un servicio en linea dónde los usuarios pueden ver el menú de una pizzeria y realizar ordenes una vez el usuario este registrado y autenticado.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; En este servicio es capaz de ver sus ordenes realizadas así como el estado de cada una con los detalles de los productos ordenados.
  

 <!--Video: [Video de demostración en Youtube](url aqui)-->

## 🛠 Skills
- HTML
- CSS
- Django
- SQLite
- JavaScript

## Detalles del proyecto
### Requerimientos solicitados
- [x] **Menu**: Tu aplicación web deberá soportar todos los elementos del menú disponibles para Pinocchio's Pizza & Subs.
- [x] **Agregando Items**: Usa Django Admin, Administradores del sitio (para los dueños del restaurante) que deberán ser capaz de agregar, actualizar y remover ítems en el menú. Agrega todos los ítems desde el menú de Pinocchio en tu base de datos usando ya sea el Admin UI o ejecutando comandos Python en el shell de Django.
- [x] **Registro, Login, Logout**: Usuarios del sitio (clientes) deberán ser capaces de registrarse para tu aplicación web con un nombre de usuario, contraseña, primer nombre, apellido, y su dirección email. Los clientes deberán luego ser capaz de acceder y salir de tu sitio web.
- [x] **Carrito de Compras**: Una vez que accedan, los usuarios deberán ver una representación del menú del restaurante, donde ellos puedan agregar ítems (según con coberturas o extras, si es apropiado) a su “carrito de compras” virtual. El contenido de las compras deberán ser guardadas incluso si el usuario cierra la ventana, o sale y vuelve acceder de nuevo.
- [x] **Colocar una Orden**: Una vez que al menos esté un ítem en el carrito de compras del usuario, ellos deberán ser capaces de colocar una orden, donde el usuario se le pregunta si confirma los ítems en el carrito de compras, y el total (¡no necesitas preocuparte sobre impuestos!) antes de colocar una orden.
- [x] **Ver Órdenes**: Los Administradores del sitio deberán tener acceso a una página donde ellos puedan ver cualquiera de las órdenes que ya se hayan solicitado.
- [x] **Toque Personal**: Agregar al menos una funcionalidad adicional de tu elección a la aplicación web. Posibles inclusiones: permitir a los Administradores del sitio de marcar las órdenes como completadas y permitir a los usuarios el ver el estado de sus órdenes pendientes o las completadas.
- [x] **En README.md** , incluye una breve reseña describiendo tu proyecto.
- [x] Si has agregado paquetes de Python que deban ser instalados para ejecutar tu aplicación web, asegúrate de agregarlos a requirements.txt.

## Instalación entorno virtual
### Crea la carpeta : 
>`py -3 -m venv .venv`   
### Activa el entorno virtual:
> `.venv\Scripts\activate`
### Instala los requerimientos: 
> `pip install -r .\requirements.txt`
### Crea las migraciones:
>`python manage.py makemigrations`
### Migra:
>`python manage.py migrate`
### Crea el super usuario:
>`python manage.py createsuperuser`
### Si no quieres cargar los productos uno a uno
>`python manage.py loaddata products.json`
## Corre la aplicación web
>`python manage.py runserver`

## Toque personal
En la vista usuario el usuario será capaz de ver un lista con todas las ordenes que ha realizado. En esta lista se muestra el precio, fecha, numero de orden y estado del pedido.
### Eliminar un pedido
En cada pedido hay un botón con el cual se puede eliminar el pedido en cuestion.
### ver detalles de un pedido
En cada pedido hay un botón con el cual un usuario sera capaz de poder ver los detalles de un pedido, esto quiere decir que podrá ver cada producto asocioado a ese pedido.