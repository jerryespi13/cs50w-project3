from django.db import models
from django.utils import timezone

# Create your models here.

class Usuarios(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    usuario = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    phone = models.CharField(max_length=12)
    direction = models.CharField(max_length=64)

    def __str__(self):
        return "f{self.firstName} {self.lastName}"
