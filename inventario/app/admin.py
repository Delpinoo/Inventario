from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Producto, Sucursal

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'sucursal')  # Muestra las columnas en la lista
    list_filter = ('sucursal',)  # Agrega el filtro por sucursal

admin.site.register(Producto)
admin.site.register(Sucursal)