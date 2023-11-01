from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# editamos el modelo user de django
class User(AbstractUser):
    picture = models.ImageField(default='user.png', upload_to='users/')
    location = models.CharField(max_length=60, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

class TamañoPizza(models.Model):
    nombre = models.CharField(max_length=6)
    
    def __str__(self):
        return f"{self.nombre}"

class TipoPizza(models.Model):
    nombre = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.nombre}"

class Pizza(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64)
    size = models.ForeignKey(TamañoPizza, on_delete=models.CASCADE, related_name="pizza")
    type = models.ForeignKey(TipoPizza, on_delete=models.CASCADE, related_name="pizza")
    price = models.FloatField()
    imagen = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.type} {self.size}"
    
