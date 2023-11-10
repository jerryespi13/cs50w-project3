let numerosExtras = 0;

let currency = "$ "

let cesta = localStorage.getItem("cart")
if(cesta === null){
    cesta = []
  }

// contenedor del carrito
let cartContainer = ""
if(document.querySelector(".productosCarrito")){
    cartContainer = document.querySelector(".productosCarrito")
}
// total del carrito
let totalCart = ""
if(document.querySelector(".totalCarrito")){
    totalCart = document.querySelector(".totalCarrito")
}
// dropdown menu 
const dropdowns = document.querySelectorAll('.dropdown');
// extras
const extras = document.querySelectorAll('.extra')
// dropdown para toppings
const dropdownsToppings = document.querySelectorAll('.dropdown-topping');

let usuario = ""
if(document.getElementById("usuario")){
    usuario = document.getElementById("usuario").innerText
}


// obtenemos csrftoken para poder trabajar con fetch
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // ¿Esta cadena de cookie comienza con el nombre que queremos?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

dropdowns.forEach(dropdown =>{
    const select = dropdown.querySelector('.select');
    const caret = dropdown.querySelector('.caret');
    const menu = dropdown.querySelector('.menu');
    const options = dropdown.querySelectorAll('.menu li');
    const selected = dropdown.querySelector('.selected');

    select.addEventListener('click', ()=>{
        select.classList.toggle('select-clicked');
        caret.classList.toggle('caret-rotate');
        menu.classList.toggle('menu-open');
    });
    options.forEach(option=>{   
        option.addEventListener('click', ()=>{
            selected.innerText = option.innerText;
            select.classList.remove('select-clicked');
            caret.classList.remove('caret-rotate');
            menu.classList.remove('menu-open');
            options.forEach(option=>{
                option.classList.remove('active');
            });
            option.classList.add('active');

            const nodoPadre = dropdown.parentNode
            const nombreProducto = nodoPadre.querySelector(".mainname2").innerText
            const idElement = parseInt(nodoPadre.querySelector(".id_producto").innerText)
            const selectedSize = option.innerText;
            const priceElement = nodoPadre.querySelector('.sideprice');

            const label = nodoPadre.querySelector(".extra");
            if(label){
                const extras = label.querySelectorAll(".inputExtra")
                extras.forEach(extra =>{
                    extra.checked = false
                })
                numerosExtras = 0
            }

            datos = {
                "idElement": idElement,
                "sizeElement": selectedSize,
                "nombreElement": nombreProducto
            }
            // actulizamos el precio en el boton
            actualizarPrecio(datos,priceElement)
        });
    });
});

// basket logo toggle
let Basket = document.querySelector(".flex-basket");
function basketshow(){
    Basket.classList.toggle("hide")
}

extras.forEach(extra =>{
    const extraSelect = extra.querySelectorAll('.inputExtra')
    extraSelect.forEach(extraClick =>{
        extraClick.addEventListener('click', ()=>{
            let extraSelected = []
            let padreNode = extraClick.parentElement.parentElement.parentElement
            let nombreProducto = padreNode.querySelector(".mainname2").innerText
            let sizeElement = padreNode.querySelector(".selected").innerHTML
            let nombreExtra = extraClick.parentElement.innerText.split(" $")[0]
            var priceElement = padreNode.querySelector(".sideprice")
            let idElement = parseInt(padreNode.querySelector(".id_producto").innerHTML)
            // si se da check en un extra, se suma el precio de ese extra
            if (extraClick.checked){
                extraSelected.push(nombreExtra)
                numerosExtras +=1
            }
            // si se descheckea un extra se resta el precio de ese extra
            else if (!extraClick.checked){
                numerosExtras -= 1
                extraSelected = []
            }
            // actualizamos el precio
            datos = {
                "idElement": idElement,
                "nombreElement": nombreProducto,
                "nombreExtra": nombreExtra,
                "sizeElement": sizeElement,
                "numerosExtras": numerosExtras,
                "extrasSelected": extraSelected
            }
            // Actualizamos el precio
            actualizarPrecio(datos, priceElement) 
        })
    })
})

dropdownsToppings.forEach(dropdownTopping =>{
    const select = dropdownTopping.querySelector('.select');
    const caret = dropdownTopping.querySelector('.caret');
    const menu = dropdownTopping.querySelector('.topping');
    const options = dropdownTopping.querySelectorAll('.topping li');
    const selected = dropdownTopping.querySelector('.selected');

    select.addEventListener('click', ()=>{
        select.classList.toggle('select-clicked');
        caret.classList.toggle('caret-rotate');
        menu.classList.toggle('menu-open');
    });
    options.forEach(option=>{   
        option.addEventListener('click', ()=>{
            selected.innerText = option.innerText;
            select.classList.remove('select-clicked');
            caret.classList.remove('caret-rotate');
            menu.classList.remove('menu-open');
            options.forEach(option=>{
                option.classList.remove('active');
            });
            option.classList.add('active');
        });
    });
});

//funcion para actualizar precio
function actualizarPrecio( datos, priceElement){
    fetch(`${window.origin}/change_Price`, {
        method: 'POST',
        headers: {
            'Content-Type': 'orders/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => priceElement.textContent = currency + data
    );
}

function printCart(){
    cartContainer.innerHTML = ""
    if(totalCart !== ""){

        totalCart.lastElementChild.innerHTML =""
    }
    cesta.forEach(product=>{
        if (product["extrasSelected"]){
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">
                                    <i class="fa fa-plus-circle" onclick="sumar (${product["idInCart"]})" aria-hidden="true"></i>
                                    ${product["cantidad"]}
                                    <i class="fa fa-minus-circle" onclick="restar(${product["idInCart"]})" aria-hidden="true"></i>
                                </div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                        <p>Extras:</p>
                                        ${product["extrasStr"]}
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                <button class="eliminarProductoCarrito" onclick="eliminar(${product["idInCart"]})" >X</button>
                            </div>`
        }
        else if(product["toppingsSelected"]){
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">
                                <i class="fa fa-plus-circle" onclick="sumar (${product["idInCart"]})" aria-hidden="true"></i>
                                ${product["cantidad"]}
                                <i class="fa fa-minus-circle" onclick="restar(${product["idInCart"]})" aria-hidden="true"></i>
                                </div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                        <p>Toppings:</p>
                                        ${product["toppingsStr"]}
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                <button class="eliminarProductoCarrito" onclick="eliminar(${product["idInCart"]})" >X</button>
                            </div>`
        }
        else{
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">
                                <i class="fa fa-plus-circle" onclick="sumar (${product["idInCart"]})" aria-hidden="true"></i>
                                ${product["cantidad"]}
                                <i class="fa fa-minus-circle" onclick="restar(${product["idInCart"]})" aria-hidden="true"></i>
                                </div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                   
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                
                                <button class="eliminarProductoCarrito" onclick="eliminar(${product["idInCart"]})" >X</button>
                            </div>`
        }
        cartContainer.lastChild.scrollIntoView(false)
        totalCart.lastElementChild.innerHTML = total()
    })
}

function clearCart() {
    cesta = [];
    printCart();
    totalCart.lastElementChild.innerHTML = ""
}

function total(){
    let total = 0
    cesta.forEach(product=>{
        let cantidad = product["cantidad"]
        let precio = product["precio"]
        let totalProduct = precio * cantidad
        total += totalProduct
    })
    return currency + total.toFixed(2)
}

function eliminar(id){
    for (let i = 0; i < cesta.length; i++){
        if (cesta[i]["idInCart"] === id){
            cesta.splice(i,1)
            break
        }
    }
    printCart();
}

function sumar(id){
    for (let i = 0; i < cesta.length; i++){
        if (cesta[i]["idInCart"] === id){
            cesta[i]["cantidad"] += 1
            break
        }
    }
    printCart();
}

function restar(id){
    for (let i = 0; i < cesta.length; i++){
        if (cesta[i]["idInCart"] === id){
            cesta[i]["cantidad"] -= 1
            if(cesta[i]["cantidad"] === 0){
                eliminar(id)
            }
            break
        }
    }
    printCart();
}

function IniciarSession(){
    window.location.href = `${window.origin}/login`
}


function salir(){
    // limpiamos el cart
    localStorage.removeItem("cart")
    cesta = []
    fetch(`${window.origin}/logout`, {
        method: 'POST',
        headers: {
            'Content-Type': 'orders/json',
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `${window.origin}/${data}`
        }
    );
}    

// add to cart
//Seleccionamos todos los botones con la class 'customisebtn2'
let buttons = document.querySelectorAll('.customisebtn2');
// ciclo para cada button
// añade el producto al carrito y el total del producto en dependencia
// de los extras o toppings seleccionados se calcula en el backend con los datos en DB
for (let i = 0; i < buttons.length; i++) {
    // agragemos un evento de escucha en cada boton
    buttons[i].addEventListener('click', function() {
        // 'this' se refiere al boton que se le dio click
        // 'closest' Busca el antecesor mas cercano que coincida con el selectot 'flex-item2'
        let container = this.closest('.flex-item2');

        // obtenemos la informacion necesaria del producto a añadir al carrito
        let datosCart = {}
        let idInCart = cesta.length + 1
        let extrasSelected = []
        let toppingsSelected = []
        let extrasStr = ""
        let toppingsStr = ""
        let idElement = container.querySelector(".id_producto").innerHTML;
        let nombreProducto = container.querySelector('.mainname2').innerText;

        // obtenemos los toppings seleccionados si tiene
        let nombresToppings = container.querySelectorAll(".topping")
        nombresToppings.forEach(nombreTopping=>{
            toppingsSelected.push(nombreTopping.querySelector(".active").innerText)
            toppingsStr += `<li>- ${nombreTopping.querySelector(".active").innerText}</li>`;
        })

        // obtenemos los extras seleccionados si tiene
        let sizeElement = container.querySelector(".selected") ? container.querySelector(".selected").innerText : ""
        let nombresExtras = container.querySelectorAll(".inputExtra");
        nombresExtras.forEach(nombreExtra=>{
            if (nombreExtra.checked){
                let extra = nombreExtra.parentElement.innerText.split(" $")[0]
                extrasSelected.push(extra)
                extrasStr += `<li>- ${extra}</li>`;
            }
        })
        datosCart = {
            "idElement": idElement,
            "idInCart": idInCart,
            "nombreElement": nombreProducto,
            "sizeElement": sizeElement,
            "cantidad": 1
        }

        if (extrasSelected.length !== 0){
            datosCart['extrasSelected'] = extrasSelected
            datosCart["extrasStr"] = extrasStr
        }

        if (toppingsSelected.length !== 0){
            datosCart['toppingsSelected'] = toppingsSelected
            datosCart["toppingsStr"] = toppingsStr
        }
        
        // validamos los datos
        fetch(`${window.origin}/cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'orders/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(datosCart)
        })
        .then(response => response.json())
        .then(data => {
            datosCart["precio"] = data
            cesta.push(datosCart)
            printCart()
            }
        );
    });
}

// guardamos el cart en localstorage
window.addEventListener('beforeunload', function (e) {
    localStorage.setItem('cart', JSON.stringify(cesta));
});

// recuperamos el cart de localstorage
document.addEventListener('DOMContentLoaded', function() {
    // Intentamos recuperar el carrito de localStorage
    let cartJSON = localStorage.getItem('cart');
    if (cartJSON) {
        // Si el carrito existe en localStorage lo convertimos de nuevo a un objeto
        cesta = JSON.parse(cartJSON);
    }
    // pintamos el carrito
    printCart()
});

function realizarPedido(){
    if (cesta.length === 0){
        cartContainer.innerHTML = `<h4 style="color: red; padding-left: 20px;">Primero añade al menos un producto en el cart</h4>`
        return
    }
    console.log(cesta)
    let dato = []
    dato.push(cesta)
    dato.push(usuario)
    console.log(cesta)
    fetch(`${window.origin}/realizar_pedido`, {
        method: 'POST',
        headers: {
            'Content-Type': 'orders/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(dato)
    })
    .then(response => response.json())
    .then(data => {console.log("pedio")
    // se limpia el cart
    cesta = []
    localStorage.removeItem("cart")
    printCart()
    window.location.href = `${window.origin}/usuario`
}
    );
}