from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio']
        widgets = {
            'nombre' : forms.TextInput(attrs={'id': 'id_nombre', 'placeholder': 'Nombre del producto'}),
            'precio' : forms.NumberInput(attrs={'id': 'id_precio', 'placeholder': 'Precio del producto'}),
        }
