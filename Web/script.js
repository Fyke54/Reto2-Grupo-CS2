// script.js
document.addEventListener('DOMContentLoaded', function() {
    
    // Pillamos los elementos del HTML
    var rangoExperiencia = document.getElementById('experiencia');
    var textoExperiencia = document.getElementById('texto-experiencia');
    var formulario = document.getElementById('formulario-principal');
    var cajaExito = document.getElementById('mensaje-exito');

    // Comprobación de seguridad para ver si encuentra la barra en la página
    if (rangoExperiencia && textoExperiencia) {
        
        // Cada vez que mueves el ratón en la barra del range
        rangoExperiencia.addEventListener('input', function() {
            // Cambia el texto del span por el valor actual de la barra
            textoExperiencia.textContent = rangoExperiencia.value;
            console.log("Años actualizados:", rangoExperiencia.value); // Esto saldrá en la consola (F12)
        });
    } else {
        console.log("Error: No se encuentra el elemento 'experiencia' o 'texto-experiencia' en el HTML.");
    }

    // Validación del formulario al pulsar el botón
    if (formulario) {
        formulario.addEventListener('submit', function(evento) {
            evento.preventDefault(); 
            
            var todoCorrecto = true; 

            // Validar Nombre
            var nombre = document.getElementById('nombre');
            var errorNombre = document.getElementById('error-nombre');
            if (nombre.value.trim() === '') {
                errorNombre.style.display = 'block';
                todoCorrecto = false;
            } else {
                errorNombre.style.display = 'none';
            }

            // Validar Email
            var email = document.getElementById('email');
            var errorEmail = document.getElementById('error-email');
            if (email.value.includes('@') === false) {
                errorEmail.style.display = 'block';
                todoCorrecto = false;
            } else {
                errorEmail.style.display = 'none';
            }