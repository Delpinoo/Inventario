from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm
from .models import Producto

def home(request):
    productos = Producto.objects.all()
    form_agregar = ProductoForm()
    form_modificar = None
    form = None
    producto = None
    formulario_activo = None
    error = None

    # Agregar producto
    if request.method == 'POST' and 'agregar_producto' in request.POST:
        formulario_activo = 'agregar'
        form_agregar = ProductoForm(request.POST)
        if form_agregar.is_valid():
            form_agregar.save()
            return redirect('index')

    # Buscar producto para modificar
    if request.method == 'POST' and 'producto_id' in request.POST and 'modificar_producto' not in request.POST:
        formulario_activo = 'modificar'
        producto_id = request.POST['producto_id']
        try:
            producto = Producto.objects.get(id=producto_id)
            form = ProductoForm(instance=producto)
        except Producto.DoesNotExist:
            return render(request, 'home/index.html', {
                'error': 'Producto no encontrado',
                'productos': productos,
                'form_agregar': form_agregar,
                'formulario_activo': formulario_activo,
            })

    # Guardar cambios
    if request.method == 'POST' and 'modificar_producto' in request.POST:
        formulario_activo = 'modificar'
        producto_id = request.POST['producto_id']
        producto = get_object_or_404(Producto, id=producto_id)
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    if request.method == 'POST' and 'eliminar_producto' in request.POST:
            formulario_activo = 'eliminar'
            producto_id = request.POST['producto_id']  # Usar ID del producto
            try:
                producto = Producto.objects.get(id=producto_id)  # Buscar por ID
                producto.delete()  # Eliminar el producto
                return redirect('index')  # Redirigir a la página principal
            except Producto.DoesNotExist:
                error = 'Producto no encontrado'  # Mensaje de error si no se encuentra

    return render(request, 'home/index.html', {
        'productos': productos,
        'form_agregar': form_agregar,
        'form': form,
        'producto': producto,
        'formulario_activo': formulario_activo,
        'error': error,
    })
