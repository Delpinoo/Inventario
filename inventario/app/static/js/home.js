function mostrarModal(tipo) {
    let modalId = '';
    
    if (tipo === 'agregar') {
        modalId = '#modal-agregar';
    } else if (tipo === 'modificar') {
        modalId = '#modal-modificar';
    } else if (tipo === 'eliminar') {
        modalId = '#modal-eliminar';
    }

    // Mostrar el modal correspondiente
    const modal = new bootstrap.Modal(document.querySelector(modalId));
    modal.show();
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

