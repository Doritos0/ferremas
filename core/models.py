from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Herramienta(models.Model):
    id_herramienta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    precio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)])
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre
    