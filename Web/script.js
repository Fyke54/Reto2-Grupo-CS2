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

            // Validar Archivo JSON
            var archivoJson = document.getElementById('archivo-json');
            var errorJson = document.getElementById('error-json');
            if (archivoJson.files.length === 0 || archivoJson.files[0].type !== 'application/json') {
                errorJson.style.display = 'block';
                todoCorrecto = false;
            } else {
                errorJson.style.display = 'none';
            }

            // Si todo está correcto
            if (todoCorrecto === true) {
                var lenguajesMarcados = document.querySelectorAll('input[name="lenguajes"]:checked');
                var bbddMarcadas = document.querySelectorAll('input[name="bbdd"]:checked');
                
                var listaLenguajes = [];
                lenguajesMarcados.forEach(function(checkbox) {
                    listaLenguajes.push(checkbox.value);
                });
                
                var listaBbdd = [];
                bbddMarcadas.forEach(function(checkbox) {
                    listaBbdd.push(checkbox.value);
                });

                var datosFormulario = {
                    nombre: nombre.value,
                    email: email.value,
                    experiencia: rangoExperiencia.value,
                    lenguajes: listaLenguajes,
                    basesDeDatos: listaBbdd,
                    nombreDelJson: archivoJson.files[0].name
                };
                
                console.log("Datos en JSON:", datosFormulario);

                cajaExito.classList.remove('oculto');
                formulario.reset();
                textoExperiencia.textContent = '0';
                
                setTimeout(function() {
                    cajaExito.classList.add('oculto');
                }, 4000);
            }
        });
    }
});