// nav bar active page
const activepage = window.location.pathname;
const navlinks = document.querySelectorAll('nav ul div a').
forEach(link =>{
    if(link.href.includes(`${activepage}`)){
        link.classList.add(`active`);
    }
});

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

            //
            var selectedSize = option.innerText;
            var smallPrice = dropdown.getAttribute('data-small-price');
            var largePrice = dropdown.getAttribute('data-large-price');

            // Determinamos el precio basado en el tamaño del producto
            var price;
            if (selectedSize === 'Small') {
                price = smallPrice;
            } 
            else if (selectedSize === 'Large') {
                price = largePrice;
            }

            // Update the price in the button
            var priceElement = dropdown.parentNode.querySelector('.sideprice');
            priceElement.textContent = '$ ' + price;
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
            let newPrice
            var nombreExtra = extraClick.parentElement.innerText.split(" $")[0]
            var priceExtra = parseFloat(extraClick.parentElement.innerText.split(" $")[1])
            var priceElement = extraClick.parentNode.parentNode.parentElement.querySelector(".sideprice")

            // si se da check en un extra, se suma el precio de ese extra
            if (extraClick.checked){
                newPrice = parseFloat(priceElement.innerHTML.split("$ ")[1]) + priceExtra
            }
            // si se descheckea un extra se resta el precio de ese extra
            else if (!extraClick.checked){
                newPrice = parseFloat(priceElement.innerHTML.split("$ ")[1]) - priceExtra
            }
            // actualizamos el precio
            priceElement.textContent = '$ ' + newPrice;
        })
    })
})
