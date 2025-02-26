from django import forms
from .models import Producto, Telefono

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'numero_serie' , 'precio', 'cantidad', 'tipo', 'sucursal']
        widgets = {
            'nombre' : forms.TextInput(attrs={'id': 'id_nombre', 'placeholder': 'Nombre del producto'}),
            'precio' : forms.NumberInput(attrs={'id': 'id_precio', 'placeholder': 'Precio del producto'}),
            'numero_serie' : forms.TextInput(attrs={'id': 'id_numero_Serie', 'placeholder': 'Número de serie'}),
        }

class TelefonoForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = ['nombre_dueño', 'modelo_telefono', 'fono', 'sucursal']
