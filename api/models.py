from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Productos(models.Model):
    TipoProducto = [
        (1, 'Herramientas Manuales'),#1- Herramientas Manuales
        (2, 'Materiales Basicos'),#2- Materiales Basicos
        (3, 'Equipo de Seguridad'), #3- Equipo de Seguridad
        (4, 'Tornillos y Anclajes'), #4-Tornillos y Anclajes
        (5, 'Fijaciones y Adhesivos'), #5-Fijaciones y Adhesivos
        (6, 'Equipos de Medicion'), #6-Equipos de Medicion
    ]
    id_producto = models.AutoField(primary_key=True)
    tipo_producto = models.IntegerField(choices=TipoProducto)
    nombre = models.CharField(max_length=25, unique=True)
    precio = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999999)])
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre