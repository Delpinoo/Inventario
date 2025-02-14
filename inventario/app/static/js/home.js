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
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

