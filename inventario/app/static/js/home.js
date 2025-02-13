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
