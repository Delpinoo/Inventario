from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_sucursal =models.CharField(max_length=100)
    direccion= models.CharField(max_length=200)
    telefono = models.CharField( max_length=50)

    def __str__(self):
        return self.nombre_sucursal
    

class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    @property
    def cantidad(self):
        """ Calcula la suma de las cantidades de los productos de este tipo """
        return self.productos.aggregate(total=models.Sum('cantidad'))['total'] or 0

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=0)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="productos")
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='productos')
    
    def __str__(self):
        return self.nombre


class Telefono(models.Model):
    nombre_dueño = models.CharField(max_length=100)
    modelo_telefono = models.CharField(max_length=100)
    fono = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^9\s\d{8}$')])
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='telefonos')
    
    def __str__(self):
        return self.nombre_dueño