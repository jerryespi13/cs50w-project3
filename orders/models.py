from django.db import models
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    usuario = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    phone = models.CharField(max_length=12)
    direction = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

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
    
