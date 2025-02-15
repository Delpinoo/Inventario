function mostrarModal(accion, id, nombre_dueño = '', modelo_telefono = '', fono = '', sucursal_id = '') {
    if (accion === 'modificar') {
        document.getElementById('modalTelefonoLabel').textContent = 'Modificar Teléfono';
        document.getElementById('telefonoId').value = id;
        document.getElementById('nombre_dueño').value = nombre_dueño;
        document.getElementById('modelo_telefono').value = modelo_telefono;
        document.getElementById('fono').value = fono;
        document.getElementById('sucursal').value = sucursal_id;
    } else {
        document.getElementById('modalTelefonoLabel').textContent = 'Agregar Teléfono';
        document.getElementById('formTelefono').reset();
    }
    var myModal = new bootstrap.Modal(document.getElementById('modalTelefono'));
    myModal.show();
}

// Función para eliminar un teléfono
function eliminarTelefono(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este teléfono?")) {
        window.location.href = "{% url 'delete_phone' 'id' %}".replace('id', id);
    }
}

// Función para eliminar varios teléfonos
function eliminarTelefonos() {
    var selected = [];
    document.querySelectorAll("input[name='telefono']:checked").forEach(function(checkbox) {
        selected.push(checkbox.value);
    });

    if (selected.length === 0) {
        alert("Por favor, selecciona al menos un teléfono para eliminar.");
        return;
    }

    if (confirm("¿Estás seguro de que deseas eliminar los teléfonos seleccionados?")) {
        var url = "{% url 'delete_multiple_phones' %}";
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = url;

        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'telefonos';
        input.value = JSON.stringify(selected);
        form.appendChild(input);
        form.appendChild(document.createElement('input')).setAttribute('name', 'csrfmiddlewaretoken').value = '{{ csrf_token }}';
        document.body.appendChild(form);
        form.submit();
    }
}