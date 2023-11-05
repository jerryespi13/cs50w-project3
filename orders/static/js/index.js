let numerosExtras = 0;

let currency = "$ "

let cart = []

const cartContainer = document.querySelector(".productosCarrito")
const totalCart = document.querySelector(".totalCarrito")



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


// dropdown menu 
const dropdowns = document.querySelectorAll('.dropdown');
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

// extras
const extras = document.querySelectorAll('.extra')
extras.forEach(extra =>{
    const extraSelect = extra.querySelectorAll('.inputExtra')
    
    extraSelect.forEach(extraClick =>{
        extraClick.addEventListener('click', ()=>{
            let padreNode = extraClick.parentElement.parentElement.parentElement
            let nombreProducto = padreNode.querySelector(".mainname2").innerText
            let sizeElement = padreNode.querySelector(".selected").innerHTML
            let nombreExtra = extraClick.parentElement.innerText.split(" $")[0]
            var priceElement = padreNode.querySelector(".sideprice")
            let idElement = parseInt(padreNode.querySelector(".id_producto").innerHTML)
            // si se da check en un extra, se suma el precio de ese extra
            if (extraClick.checked){
                numerosExtras +=1
            }
            // si se descheckea un extra se resta el precio de ese extra
            else if (!extraClick.checked){
                numerosExtras -= 1
            }
            // actualizamos el precio
            datos = {
                "idElement": idElement,
                "nombreElement": nombreProducto,
                "nombreExtra": nombreExtra,
                "sizeElement": sizeElement,
                "numerosExtras": numerosExtras
            }
            // Actualizamos el precio
            actualizarPrecio(datos, priceElement) 
        })
    })
})

// dropdown para toppings
const dropdownsToppings = document.querySelectorAll('.dropdown-topping');
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

// add to cart
//Seleccionamos todos los botones con la class 'customisebtn2'
var buttons = document.querySelectorAll('.customisebtn2');

// ciclo para cada button
for (var i = 0; i < buttons.length; i++) {
    // agragemos un evento de escucha en cada boton
    buttons[i].addEventListener('click', function() {
        // 'this' se refiere al boton que se le dio click
        // 'closest' Busca el antecesor mas cercano que coincida con el selectot 'flex-item2'
        var container = this.closest('.flex-item2');

        // obtenemos la informacion necesaria del producto a añadir al carrito
        let datosCart = {}
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
            "nombreElement": nombreProducto,
            "sizeElement": sizeElement
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
            cart.push(datosCart)
            printCart()
            }
        );
    });
}

function printCart(){
    let totalPrice = 0
    cartContainer.innerHTML = ""
    cart.forEach(product=>{
        totalPrice = totalPrice + parseFloat(product["precio"])
        if (product["extrasSelected"]){
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">1</div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                        <p>Extras:</p>
                                        ${product["extrasStr"]}
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                <button class="eliminarProductoCarrito">X</button>
                            </div>`
        }
        else if(product["toppingsSelected"]){
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">1</div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                        <p>Toppings:</p>
                                        ${product["toppingsStr"]}
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                <button class="eliminarProductoCarrito">X</button>
                            </div>`
        }
        else{
            cartContainer.innerHTML += `
                            <div class="productoCarrito">
                                <div class="cantidadProductoCarrito">1</div>
                                <div class="descriptionProductoCarrito">
                                    <div class="nombreProductoCarrito">${product["nombreElement"]}</div>
                                    <ul class="extrasProductosCarritos">
                                   
                                    </ul>
                                </div>
                                <div class="tamañoProductoCarrito">${product["sizeElement"]}</div>
                                <div class="precioProductoCarrito">$ ${product["precio"]}</div>
                                <button class="eliminarProductoCarrito">X</button>
                            </div>`
        }
        cartContainer.lastChild.scrollIntoView(false)
        totalCart.lastElementChild.innerHTML = currency + totalPrice.toFixed(2)
    })
}

function clearCart() {
    cart = [];
    printCart();
    totalCart.lastElementChild.innerHTML = ""
}