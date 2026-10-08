from django.db import models
from django.core.validators import MinValueValidator

class Mascota(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Mascota")
    especie = models.CharField(max_length=50, help_text="Ej: Perro, Gato, Ave")
    raza = models.CharField(max_length=50, blank=True, null=True)
    edad = models.PositiveIntegerField(help_text="Edad en años")
    precio = models.IntegerField(validators=[MinValueValidator(1)], help_text="Precio mayor a 0")
    stock = models.IntegerField(validators=[MinValueValidator(0)], help_text="Stock no puede ser negativo")

    def __str__(self):
        return f"{self.nombre} - {self.especie}"