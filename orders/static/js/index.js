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
    let numerosExtras = 0;
    extraSelect.forEach(extraClick =>{
        extraClick.addEventListener('click', ()=>{
            let padreNode = extraClick.parentElement.parentElement.parentElement
            const nombreProducto = padreNode.querySelector(".mainname2").innerText
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
    .then(data => priceElement.textContent = '$ ' + data
    );
}