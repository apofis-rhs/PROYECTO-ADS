document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. VALIDACIÓN DINÁMICA DE NIVEL/TUTOR
    // ==========================================
    const selectNivel = document.querySelector('select[name="nivel"]');
    const selectTutor = document.querySelector('select[name="tutor"]');

    if (selectNivel && selectTutor) {
        const contenedorTutor = selectTutor.closest('.col-8') || selectTutor.parentElement;
        const labelTutor = contenedorTutor.querySelector('label');

        function validarNivel() {
            const nivelId = parseInt(selectNivel.value);
            if (isNaN(nivelId)) {
                // Si no hay nivel, forzamos requerir tutor por seguridad
                selectTutor.required = true;
                return;
            }
            // 1-3: Básica (Obligatorio) | 4-5: Superior (Opcional)
            if (nivelId >= 1 && nivelId <= 3) {
                selectTutor.required = true;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado *";
            } else if (nivelId >= 4) {
                selectTutor.required = false;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado (Opcional)";
            }
        }

        selectNivel.addEventListener('change', validarNivel);
        // Ejecutar al inicio por si es una edición
        validarNivel(); 
    }


    // ==========================================
    // 2. CONFIRMACIÓN DE BAJA
    // ==========================================
    const formBaja = document.getElementById('formBaja');

    if (formBaja) {
        formBaja.addEventListener('submit', function(event) {
            const opcionSeleccionada = document.querySelector('input[name="tipoBaja"]:checked');
            if (!opcionSeleccionada) return; 

            const tipoBaja = opcionSeleccionada.value;
            let mensaje = "";

            if (tipoBaja === 'definitiva') {
                mensaje = "⚠️ ALERTA DE SEGURIDAD ⚠️\n\nEstás a punto de ELIMINAR PERMANENTEMENTE a este alumno.\nEsta acción NO se puede deshacer.\n\n¿Estás realmente seguro de continuar?";
            } else {
                mensaje = "¿Confirmas que deseas dar de BAJA TEMPORAL a este alumno?";
            }
            
            const confirmado = confirm(mensaje);
            if (!confirmado) {
                event.preventDefault();
            }
        });
    }

    // ==========================================
    // 3. REGISTRAR NUEVO TUTOR DESDE MODAL
    // ==========================================
    const formTutor = document.getElementById('formNuevoTutor');

    if (formTutor) {
        formTutor.addEventListener('submit', function(e) {
            e.preventDefault(); 
            const apiUrl = this.getAttribute('data-api-url');
            const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;
            let formData = new FormData(this);
            
            fetch(apiUrl, { 
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrfToken }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    var modalElem = document.getElementById('modalNuevoTutor');
                    var modalInstance = bootstrap.Modal.getInstance(modalElem);
                    modalInstance.hide();
                    formTutor.reset();

                    let selectTutor = document.getElementById('selectTutor');
                    let option = new Option(data.tutor_nombre, data.tutor_id);
                    selectTutor.add(option);
                    selectTutor.value = data.tutor_id;

                    alert('Tutor registrado correctamente. Continúe con el registro del alumno.');
                } else {
                    let errorDiv = document.getElementById('msgErrorTutor');
                    errorDiv.innerText = "Error: " + data.error;
                    errorDiv.style.display = 'block';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // ==========================================
    // 4. GENERACIÓN DE DOCUMENTOS (PDF) - COMBOBOX
    // ==========================================
    const btnVisualizar = document.getElementById('btnVisualizarDoc');
    const btnDescargar = document.getElementById('btnDescargarDoc');
    const selectDoc = document.getElementById('selectDocumento');

    function abrirDocumento(downloadMode) {
        const tipo = selectDoc.value;
        const baseUrl = btnVisualizar.getAttribute('data-url'); 
        
        if (!tipo) {
            alert('Por favor, seleccione un tipo de documento de la lista.');
            return;
        }
        let finalUrl = `${baseUrl}?tipo=${tipo}`;
        if (downloadMode) { finalUrl += '&download=true'; }

        window.open(finalUrl, '_blank');
    }

    if (btnVisualizar && selectDoc) {
        btnVisualizar.addEventListener('click', function() { abrirDocumento(false); });
    }

    if (btnDescargar && selectDoc) {
        btnDescargar.addEventListener('click', function() { abrirDocumento(true); });
    }

    // ==========================================
    // 5. IMPRIMIR FICHA TÉCNICA (Botón Individual)
    // ==========================================
    const btnFicha = document.getElementById('btnImprimirFicha');

    if (btnFicha) {
        console.log("Botón ficha encontrado, agregando evento..."); // Debug en consola
        btnFicha.addEventListener('click', function() {
            const baseUrl = this.getAttribute('data-url');
            window.open(`${baseUrl}?tipo=ficha`, '_blank');
        });
    }

});