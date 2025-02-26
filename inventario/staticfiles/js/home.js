function mostrarModal(tipo, id, nombre, numero_serie, precio, cantidad, tipoProducto, sucursal) {
    console.log('Tipo:', tipo);  // Debe ser 'modificar' o 'agregar'
    console.log('ID:', id);
    console.log('Nombre:', nombre);
    console.log('Número de serie', numero_serie)
    console.log('Precio:', precio);
    console.log('Cantidad:', cantidad);
    console.log('Tipo Producto:', tipoProducto); // Aquí debe mostrarse 'Electrónica'
    console.log('Sucursal:', sucursal);
    
    if (tipo === 'modificar') {
        document.querySelector('#producto-id').value = id;
        document.querySelector('#nombre').value = nombre;
        document.querySelector('#numero_serie').value = numero_serie;
        document.querySelector('#precio').value = precio;
        document.querySelector('#cantidad').value = cantidad;
        document.querySelector('#tipo').value = tipoProducto;  // ✅ Corregido
        document.querySelector('#sucursal').value = sucursal;  

        // Verificar si la opción de sucursal existe, si no, agregarla
        let sucursalSelect = document.querySelector('#sucursal');
        let optionExists = false;

        for (let option of sucursalSelect.options) {
            if (option.value === sucursal) {
                optionExists = true;
                break;
            }
        }

        if (!optionExists) {
            let newOption = new Option(sucursal, sucursal);
            sucursalSelect.add(newOption);
        }
        
        sucursalSelect.value = sucursal;

        const modal = new bootstrap.Modal(document.querySelector('#modal-modificar'));
        modal.show();
    }

    if (tipo === 'agregar') {
        document.querySelector('#nombre').value = '';
        document.querySelector('#producto-id').value = '';
        document.querySelector('#numero_serie').value = '';
        document.querySelector('#precio').value = '';
        document.querySelector('#cantidad').value = '';
        document.querySelector('#tipo').value = '';
        document.querySelector('#sucursal').value = sucursal;

        const modal = new bootstrap.Modal(document.querySelector('#modal-agregar'));
        modal.show();
    }
}


function eliminarProductos() {
    const productosSeleccionados = document.querySelectorAll('input[name="producto"]:checked');
    
    if (productosSeleccionados.length === 0) {
        alert('Por favor, selecciona al menos un producto para eliminar.');
        return;
    }

    // Confirmación antes de eliminar
    const confirmar = confirm('¿Estás seguro de que deseas eliminar los productos seleccionados?');
    if (confirmar) {
        // Obtener los IDs de los productos seleccionados
        const idsProducto = Array.from(productosSeleccionados).map(producto => producto.value);
        
        // Enviar la solicitud al servidor para eliminar los productos
        fetch('/eliminar-productos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ ids: idsProducto })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Hubo un error al eliminar los productos');
            }
            return response.json();
        })
        .then(data => {
            // Lógica de éxito
            console.log('Productos eliminados:', data);

            // Eliminar los productos seleccionados del DOM
            productosSeleccionados.forEach(producto => {
                const productoElemento = producto.closest('tr');  // Suponiendo que cada producto está dentro de un <tr>
                if (productoElemento) {
                    productoElemento.remove();  // Elimina la fila correspondiente al producto
                }
            });

            // Opcional: Actualizar el conteo de productos o realizar otras acciones de UI
            actualizarConteoProductos();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function actualizarConteoProductos() {
    const productosRestantes = document.querySelectorAll('input[name="producto"]').length;
    const contadorProductos = document.getElementById('contador-productos'); // Asumiendo que tienes un elemento con este ID para mostrar el conteo

    if (contadorProductos) {
        contadorProductos.textContent = `Productos restantes: ${productosRestantes}`;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const checkAll = document.getElementById('check-all');
    
    if (checkAll) {
        checkAll.addEventListener('change', function(event) {
            // Obtener todas las checkboxes de productos
            const checkboxes = document.querySelectorAll('input[name="producto"]');
            
            // Seleccionar o desmarcar todas las checkboxes de productos
            checkboxes.forEach(checkbox => {
                checkbox.checked = event.target.checked;
            });
        });
    } else {
        console.error('El checkbox con el id "check-all" no existe.');
    }
});
/*
document.getElementById('formModificar').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Obtener los valores del formulario
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const sucursal = document.getElementById('sucursal').value;
    
    // Aquí puedes agregar la lógica para enviar los datos al servidor para guardar los cambios
    console.log('Datos modificados:', { nombre, precio, sucursal });
});
*/