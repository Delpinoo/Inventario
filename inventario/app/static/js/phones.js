function abrirModalEditar(telefonoId, nombre, modelo, fono, sucursalId) {
    document.getElementById('telefonoIdEditar').value = telefonoId;
    document.getElementById('nombre_dueño_editar').value = nombre;
    document.getElementById('modelo_telefono_editar').value = modelo;
    document.getElementById('fono_editar').value = fono;
    document.getElementById('sucursal_editar').value = sucursalId;

    document.getElementById('formEditarTelefono').action = `/modificar_telefono/${telefonoId}/`;

    let modal = new bootstrap.Modal(document.getElementById('modalEditarTelefono'));
    modal.show();
}

function openAddPhoneModal() {
    document.getElementById("formTelefono").reset();

    const modal = new bootstrap.Modal(document.getElementById('modalTelefono'));
    modal.show();
}

document.getElementById('formEditarTelefono').addEventListener('submit', function (event) {
    event.preventDefault();
    let telefonoId = document.getElementById('telefonoIdEditar').value;
    this.action = `/modificar_telefono/${telefonoId}/`;
    this.submit();
});


function eliminar_telefono() {
    const checkboxes = document.querySelectorAll('.telefono-checkbox:checked');
    const idsSeleccionados = [];

    checkboxes.forEach((checkbox) => {
        idsSeleccionados.push(checkbox.value);
    });

    if (idsSeleccionados.length === 0) {
        alert('Por favor, selecciona al menos un teléfono.');
        return;
    }

    fetch('/eliminar_telefonos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({ ids: idsSeleccionados })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        if (data.success) {
            alert('Los teléfonos seleccionados han sido eliminados');
            location.reload();  
        } else {
            alert('No se pudo eliminar el teléfono. ' + (data.message || ''));
        }
    })
    .catch(error => {
        console.error('Error al eliminar teléfonos:', error);
        alert('Ocurrió un error al intentar eliminar los teléfonos.');
    });
}

function toggleCheckboxes() {
    const checkAll = document.getElementById('check-all');
    const checkboxes = document.querySelectorAll('.telefono-checkbox');

    checkboxes.forEach(function(checkbox) {
        checkbox.checked = checkAll.checked;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function seleccionar_todos() {
    const checkboxes = document.querySelectorAll('.telefono-checkbox');
    const checkAll = document.getElementById('check-all');
    
    checkboxes.forEach((checkbox) => {
        checkbox.checked = checkAll.checked;
    });
}