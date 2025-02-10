function mostrarFormulario(formularioId) {
    // Ocultar todos los formularios
    const formularios = document.querySelectorAll('.container-forms, .search-producto');
    formularios.forEach(formulario => {
        formulario.classList.remove('visible');
        formulario.classList.add('oculto');
    });

    // Mostrar el formulario seleccionado
    const formularioSeleccionado = document.getElementById(`form-${formularioId}`);
    if (formularioSeleccionado) {
        formularioSeleccionado.classList.remove('oculto');
        formularioSeleccionado.classList.add('visible');
    } else {
        console.error(`Formulario con ID 'form-${formularioId}' no encontrado.`);
    }
}
