from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ProductoForm
from .models import Producto, Sucursal
from django.conf import settings
from datetime import datetime
from openpyxl.cell.cell import Cell
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import openpyxl
import os
import json


def escribir_valor(ws, fila, columna, valor):
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
    productos = Producto.objects.none()
    form_agregar = ProductoForm()
    form_modificar = None
    form = None
    producto = None
    formulario_activo = None
    error = None
    sucursales = Sucursal.objects.all()

    sucursal_id = request.GET.get('sucursal', None)  # Si no hay 'sucursal', será None
    # Si no hay sucursal seleccionada, mostrar todos los productos
    if sucursal_id:
        productos = Producto.objects.filter(sucursal_id=sucursal_id)
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no hay filtro de sucursal



    # Agregar producto
    if request.method == 'POST' and 'agregar_producto' in request.POST:
        formulario_activo = 'agregar'
        form_agregar = ProductoForm(request.POST)
        if form_agregar.is_valid():
            producto = form_agregar.save(commit=False)
            producto.sucursal_id = sucursal_id  # Asignar la sucursal filtrada al producto
            producto.save()
            return redirect(f"{request.path}?sucursal={sucursal_id}")

    if request.method == 'POST' and 'agregar_producto' in request.POST:
            formulario_activo = 'agregar'
            form_agregar = ProductoForm(request.POST)
            if form_agregar.is_valid():
                producto = form_agregar.save(commit=False)
                producto.sucursal_id = sucursal_id
                producto.save()
                return redirect(f"{request.path}?sucursal={sucursal_id}")

    if request.GET.get('exportar', False):  
        sucursal_id = request.GET.get('sucursal')
    
        if not sucursal_id:
            return HttpResponse("Error: No se ha proporcionado el ID de la sucursal", status=400)

        try:
            sucursal = Sucursal.objects.get(id=sucursal_id)
        except Sucursal.DoesNotExist:
            return HttpResponse(f"Error: No se encontró la sucursal con ID {sucursal_id}", status=404)
        
        plantilla_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'templates', 'plantilla_inventario.xlsx')
        
        if not os.path.exists(plantilla_path):
            return HttpResponse(f"Error: El archivo plantilla no se encuentra en la ruta {plantilla_path}", status=404)

        wb = openpyxl.load_workbook(plantilla_path)
        ws = wb.active

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        escribir_valor(ws, 11, 12, fecha_actual)

        ws['L11'] = fecha_actual

        sucursal = Sucursal.objects.get(id=sucursal_id) 
    
        nombre_sucursal = sucursal.nombre_sucursal
        direccion = sucursal.direccion
        telefono = sucursal.telefono


        escribir_valor(ws, 38, 5, nombre_sucursal)
        escribir_valor(ws, 38, 8, direccion)
        escribir_valor(ws, 38, 11, telefono)
        
        productos = Producto.objects.filter(sucursal=sucursal)

        total = sum(producto.precio for producto in productos)      
        for row_num, producto in enumerate(productos, start=14):
            escribir_valor(ws, row_num, 4, producto.nombre)  
            escribir_valor(ws, row_num, 5, f"${producto.precio}")  

        escribir_valor(ws, 14, 6, f"${total}")
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=inventario_actualizado.xlsx'
        wb.save(response)
        print("Sucursal ID:", sucursal_id)
        print("Ruta de plantilla:", plantilla_path)
        return response
        
        
    return render(request, 'home/index.html', {
        'productos': productos,
        'form_agregar': form_agregar,
        'form': form,
        'producto': producto,
        'formulario_activo': formulario_activo,
        'error': error,
        'sucursales': sucursales,
    })



def eliminar_productos(request):
    if request.method == 'POST':
        try:
            # Obtener los IDs de los productos a eliminar desde el cuerpo de la solicitud
            data = json.loads(request.body)
            ids_producto = data.get('ids', [])
            
            # Lógica para eliminar los productos (aquí debes agregar tu lógica real)
            for producto_id in ids_producto:
                producto = Producto.objects.get(id=producto_id)
                producto.delete()
            
            # Si todo va bien, devolver un mensaje de éxito
            return JsonResponse({'success': True})
        except Exception as e:
            # En caso de error, devolver el mensaje de error
            return JsonResponse({'success': False, 'error': str(e)})
        
def modificar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')

        producto = get_object_or_404(Producto, id=producto_id)
        
        # Actualizar los campos del producto
        producto.nombre = nombre
        producto.precio = precio
        producto.save()

        # Redirigir a la página donde se muestra el inventario
        return redirect('home')  # Puedes redirigir a cualquier vista que quieras después de modificar

    return render(request, 'nombre_del_template.html')
