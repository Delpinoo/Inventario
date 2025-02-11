from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ProductoForm
from .models import Producto
from django.conf import settings
from datetime import datetime
from openpyxl.cell.cell import Cell
import openpyxl
import os


def escribir_valor(ws, fila, columna, valor):
    """
    Escribe un valor en una celda asegurando que no sea una MergedCell
    """
    cell = ws.cell(row=fila, column=columna)
    if isinstance(cell, Cell) and not isinstance(cell, openpyxl.cell.cell.MergedCell):
        cell.value = valor
    else:
        # Encontrar la celda principal de la fusión
        for rango in ws.merged_cells.ranges:
            if (cell.coordinate in rango):
                superior_izquierda = rango.min_row, rango.min_col
                ws.cell(row=superior_izquierda[0], column=superior_izquierda[1]).value = valor
                break 
            

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


        # Verifica si la solicitud es para descargar el Excel
    if request.GET.get('exportar', False):  # Si la URL tiene '?exportar=true'
        # Cargar la plantilla de Excel
            plantilla_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'templates', 'plantilla_inventario.xlsx')
        
        # Verificar si el archivo realmente existe en esa ruta
            if not os.path.exists(plantilla_path):
                return HttpResponse(f"Error: El archivo plantilla no se encuentra en la ruta {plantilla_path}", status=404)

            wb = openpyxl.load_workbook(plantilla_path)
            ws = wb.active

                # Obtener la fecha actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato de fecha y hora
            escribir_valor(ws, 11, 12, fecha_actual)

            # Colocar la fecha de impresión en la celda L11
            ws['L11'] = fecha_actual


            # Consultar productos de la base de datos
            productos = Producto.objects.all()

            # Empezar a agregar los datos a partir de la fila 3 (puedes ajustarlo según tu plantilla)
            total = sum(producto.precio for producto in productos)      
            for row_num, producto in enumerate(productos, start=14):
                escribir_valor(ws, row_num, 4, producto.nombre)  # Columna C: Nombre
                escribir_valor(ws, row_num, 5, producto.precio)  # Columna D: Precio 

            escribir_valor(ws, 14, 6, f"${total}")
            # Generar la respuesta HTTP
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=inventario_actualizado.xlsx'
            wb.save(response)
            return response


    productos = Producto.objects.all()
    return render(request, 'home/index.html', {
        'productos': productos,
        'form_agregar': form_agregar,
        'form': form,
        'producto': producto,
        'formulario_activo': formulario_activo,
        'error': error,
    })
