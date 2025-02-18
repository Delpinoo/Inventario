from django import forms
from .models import Producto, Telefono

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'cantidad', 'tipo', 'sucursal']
        widgets = {
            'nombre' : forms.TextInput(attrs={'id': 'id_nombre', 'placeholder': 'Nombre del producto'}),
            'precio' : forms.NumberInput(attrs={'id': 'id_precio', 'placeholder': 'Precio del producto'}),
        }

class TelefonoForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = ['nombre_dueño', 'modelo_telefono', 'fono', 'sucursal']
