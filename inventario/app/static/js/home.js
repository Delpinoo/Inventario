function mostrarModal(tipo, id, nombre, numero_serie, precio, cantidad, tipoProducto, sucursal) {
    console.log('Tipo:', tipo);  
    console.log('ID:', id);
    console.log('Nombre:', nombre);
    console.log('Número de serie', numero_serie)
    console.log('Precio:', precio);
    console.log('Cantidad:', cantidad);
    console.log('Tipo Producto:', tipoProducto); 
    console.log('Sucursal:', sucursal);
    
    if (tipo === 'modificar') {
        document.querySelector('#producto-id').value = id;
        document.querySelector('#nombre').value = nombre;
        document.querySelector('#numero_serie').value = numero_serie;
        document.querySelector('#precio').value = precio;
        document.querySelector('#cantidad').value = cantidad;
        document.querySelector('#tipo').value = tipoProducto;  
        document.querySelector('#sucursal').value = sucursal;  

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

    const confirmar = confirm('¿Estás seguro de que deseas eliminar los productos seleccionados?');
    if (confirmar) {
        const idsProducto = Array.from(productosSeleccionados).map(producto => producto.value);
        
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

            productosSeleccionados.forEach(producto => {
                const productoElemento = producto.closest('tr');  
                if (productoElemento) {
                    productoElemento.remove();  
                }
            });

            actualizarConteoProductos();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function actualizarConteoProductos() {
    const productosRestantes = document.querySelectorAll('input[name="producto"]').length;
    const contadorProductos = document.getElementById('contador-productos');

    if (contadorProductos) {
        contadorProductos.textContent = `Productos restantes: ${productosRestantes}`;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const checkAll = document.getElementById('check-all');
    
    if (checkAll) {
        checkAll.addEventListener('change', function(event) {
            const checkboxes = document.querySelectorAll('input[name="producto"]');
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = event.target.checked;
            });
        });
    } else {
        console.error('El checkbox con el id "check-all" no existe.');
    }
});