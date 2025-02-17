function abrirModalEditar(telefonoId, nombre, modelo, fono, sucursalId) {
    document.getElementById('telefonoIdEditar').value = telefonoId;
    document.getElementById('nombre_dueño_editar').value = nombre;
    document.getElementById('modelo_telefono_editar').value = modelo;
    document.getElementById('fono_editar').value = fono;
    document.getElementById('sucursal_editar').value = sucursalId;

    // Cambiar dinámicamente la acción del formulario
    document.getElementById('formEditarTelefono').action = `/modificar_telefono/${telefonoId}/`;

    let modal = new bootstrap.Modal(document.getElementById('modalEditarTelefono'));
    modal.show();
}

document.getElementById('formEditarTelefono').addEventListener('submit', function (event) {
    event.preventDefault();
    let telefonoId = document.getElementById('telefonoIdEditar').value;
    this.action = `/modificar_telefono/${telefonoId}/`;
    this.submit();
});

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