from django.db import models

# Create your models here.

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_sucursal =models.CharField(max_length=100)
    direccion= models.CharField(max_length=200)
    telefono = models.CharField( max_length=50)

    def __str__(self):
        return self.nombre_sucursal
    

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="productos", default=1)
    
    def __str__(self):
        return self.nombre
    