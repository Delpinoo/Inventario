
function mostrarModal(tipo, id, nombre, precio, sucursal) {
    console.log('Tipo:', tipo);
    console.log('ID:', id);
    console.log('Nombre:', nombre);
    console.log('Precio:', precio);
    console.log('Sucursal:', sucursal);
    
    // Ahora puedes usar estos valores para llenar el formulario en tu modal.
    if (tipo === 'modificar') {
        // Supongamos que el modal tiene campos con id #nombre, #precio, y #sucursal.
        document.querySelector('#nombre').value = nombre;
        document.querySelector('#precio').value = precio;
        document.querySelector('#producto-id').value = id; 
        
        // Aquí puedes abrir el modal.
        const modal = new bootstrap.Modal(document.querySelector('#modal-modificar'));
        modal.show();
    }
    
    if (tipo === 'agregar') {
        // Supongamos que el modal tiene campos con id #nombre, #precio, y #sucursal.
        document.querySelector('#nombre').value = nombre;
        document.querySelector('#precio').value = precio;
        document.querySelector('#sucursal').value = sucursal;

        
        // Aquí puedes abrir el modal.
        const modal = new bootstrap.Modal(document.querySelector('#modal-agregar'));
        modal.show();
    }

}


/*
function mostrarModal(id, nombre, precio, sucursal) {
    // Rellenar los campos del modal con la información del producto
    document.getElementById('nombre').value = nombre;
    document.getElementById('precio').value = precio;
    document.getElementById('sucursal').value = sucursal;

    // Mostrar el modal
    var modal = new bootstrap.Modal(document.getElementById('modalModificar'));
    modal.show();
}
*/

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