from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# editamos el modelo user de django
class User(AbstractUser):
    picture = models.ImageField(default='user.png', upload_to='users/')
    location = models.CharField(max_length=60, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

# tabla tamaños
class Tamaño(models.Model):
    nombre = models.CharField(max_length=6)
    
    def __str__(self):
        return f"{self.nombre}"

# tabla toppings
class Topping(models.Model):
    nombre = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nombre}"

class Pizza(models.Model):
    name = models.CharField(max_length=64)
    sizes = models.ManyToManyField(Tamaño, related_name="pizza")    
    large_price = models.DecimalField(max_digits=5, decimal_places=2)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    numeroDeToppings = models.IntegerField(max_length=1, default=0)
    topping = models.ManyToManyField(Topping, related_name="pizza", blank=True, null=True)
    imagen = models.ImageField(default='pizza.jpg', upload_to='productos/')
    description = models.TextField(max_length=255)

    class Meta:
        db_table = 'Pizza'

    def __str__(self):
        return f"{self.name}"
    

# tabla extras
class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    def __str__(self) -> str:
        return f"{self.name}"

# tabla subs
class Sub(models.Model):
    name  = models.CharField(max_length=64)
    sizes = models.ManyToManyField(Tamaño, related_name="subs")
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=255, null=True, blank=True)
    extras = models.ManyToManyField(Extra, blank=True, related_name="sub")
    imagen = models.ImageField(default='sub.png', upload_to='productos/')

    class Meta:
        db_table = 'Sub'

    def __str__(self):
        return f"{self.name}"

# tabla dinner plates
class DinnerPlate(models.Model):
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=5, decimal_places=2)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)
    sizes = models.ManyToManyField(Tamaño, related_name="dinners")
    description = models.TextField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(default='dinner.jpg', upload_to='productos/')

    class Meta:
        db_table = 'DinnerPlate'

    def __str__(self):
        return f"{self.name}"

# tabla Salads    
class Salads(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(default='salads.avif', upload_to='productos/')

    class Meta:
        db_table = 'Salads'

    def __str__(self):
        return f"{self.name}"
    
# tabla Pasta
class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(default='pasta.jpg', upload_to='productos/')

    class Meta:
        db_table = 'Pasta'

    def __str__(self):
        return f"{self.name}"
    
# tabla ordenes
class Orden(models.Model):
    ESTADOS = (
         ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('R', 'Recibido'),
        ('C', 'Cancelado')
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    

    def __str__(self):
        return f'Orden #{self.id} - {self.usuario.username} - {self.get_estado_display()}'
    
# productos agregados en cada orden
class OrdenProducto(models.Model):
    orden = models.ForeignKey(Orden, related_name='productos', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, null=True, blank=True, on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub, null=True, blank=True, on_delete=models.CASCADE)
    pasta = models.ForeignKey(Pasta, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.name} en Orden #{self.orden.id}'