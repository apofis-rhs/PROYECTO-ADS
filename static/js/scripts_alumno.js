document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. AÑADIR/EDITAR ALUMNO
    // ==========================================
    const selectNivel = document.querySelector('select[name="nivel"]');
    const selectTutor = document.querySelector('select[name="tutor"]');

    // Solo ejecutamos esto si existen los elementos (estamos en la pantalla de Añadir)
    if (selectNivel && selectTutor) {
        
        // Buscamos el label del tutor
        const contenedorTutor = selectTutor.closest('.col-8') || selectTutor.parentElement;
        const labelTutor = contenedorTutor.querySelector('label');

        function validarNivel() {
            const nivelId = parseInt(selectNivel.value);

            if (isNaN(nivelId)) {
                selectTutor.required = true;
                return;
            }

            // Lógica: 1-3 (Básico) -> Obligatorio | 4-5 (Superior) -> Opcional
            if (nivelId >= 1 && nivelId <= 3) {
                selectTutor.required = true;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado *";
            } else if (nivelId >= 4) {
                selectTutor.required = false;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado (Opcional)";
            }
        }

        selectNivel.addEventListener('change', validarNivel);
        validarNivel(); // Ejecutar al cargar
    }


    // ==========================================
    // 2. BAJA DE ALUMNO
    // ==========================================
    const formBaja = document.getElementById('formBaja');

    // Solo ejecutamos esto si existe el formulario de baja (estamos en pantalla Baja)
    if (formBaja) {
        
        formBaja.addEventListener('submit', function(event) {
            // Buscamos qué opción seleccionó
            const opcionSeleccionada = document.querySelector('input[name="tipoBaja"]:checked');
            
            if (!opcionSeleccionada) return; // Por si acaso

            const tipoBaja = opcionSeleccionada.value;
            let mensaje = "";

            if (tipoBaja === 'definitiva') {
                mensaje = "⚠️ ALERTA DE SEGURIDAD ⚠️\n\nEstás a punto de ELIMINAR PERMANENTEMENTE a este alumno.\nEsta acción NO se puede deshacer.\n\n¿Estás realmente seguro de continuar?";
            } else {
                mensaje = "¿Confirmas que deseas dar de BAJA TEMPORAL a este alumno?";
            }

            // Mostramos la confirmación
            const confirmado = confirm(mensaje);

            if (!confirmado) {
                // Si el usuario cancela, evitamos que el formulario se envíe
                event.preventDefault();
            }
        });
    }

});