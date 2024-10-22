# my_app/models/user.py
from django.db import models

class Recolector(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    password = models.CharField(max_length=255)
    nombre = models.CharField(null=True, blank=True)
    apellido = models.CharField(null=True, blank=True)
    saldo = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.dni
