document.addEventListener('DOMContentLoaded', function() {
    console.log("JS de Alumno cargado y operativo.");

    // ==========================================
    // 1. SELECTORES GLOBALES
    // ==========================================
    const formularioAlumno = document.querySelector('form:not(#formNuevoTutor)');
    const inputBoleta = document.querySelector('input[name="boleta"]');
    const mensajeErrorBoleta = document.getElementById('errorBoleta');
    const selectNivel = document.querySelector('select[name="nivel"]');
    const selectTutor = document.querySelector('select[name="tutor"]');
    const inputFecha = document.querySelector('input[name="fecha_nacimiento"]');
    const mensajeErrorEdad = document.getElementById('errorEdadNivel');
    const inputCurp = document.querySelector('input[name="curp"]');
    const mensajeErrorCurp = document.getElementById('errorCurp');
    const camposTelefono = document.querySelectorAll('input[name*="telefono"]');

    // ==========================================
    // 2. VALIDACIÓN DE BOLETA (AAAA430###)
    // ==========================================
    if (inputBoleta) {
        inputBoleta.addEventListener('input', function() {
            const valor = this.value.trim();
            const añoActual = new Date().getFullYear();
            const regexBoleta = /^\d{4}430\d{3}$/;
            
            if (valor !== "") {
                if (!regexBoleta.test(valor)) {
                    this.classList.add('is-invalid');
                    if (mensajeErrorBoleta) {
                        mensajeErrorBoleta.textContent = "Formato inválido: Año(4) + 430 + 3 dígitos.";
                        mensajeErrorBoleta.style.display = 'block';
                    }
                } else {
                    const añoIngreso = parseInt(valor.substring(0, 4));
                    if (añoIngreso > añoActual) {
                        this.classList.add('is-invalid');
                        if (mensajeErrorBoleta) {
                            mensajeErrorBoleta.textContent = `El año (${añoIngreso}) no puede ser mayor al actual.`;
                            mensajeErrorBoleta.style.display = 'block';
                        }
                    } else {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                        if (mensajeErrorBoleta) mensajeErrorBoleta.style.display = 'none';
                    }
                }
            } else {
                this.classList.remove('is-invalid');
                if (mensajeErrorBoleta) mensajeErrorBoleta.style.display = 'none';
            }
        });
    }

   // ==========================================
// ==========================================
// 3. VALIDACIÓN DE CURP (GLOBAL Y DINÁMICA)
// ==========================================
const regexCurp = /^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM][A-Z]{5}\d$/;

// Usamos delegación de eventos en el document para capturar inputs de cualquier CURP
document.addEventListener('input', function (e) {
    if (e.target.classList.contains('curp-input')) {
        let input = e.target;
        // Convertir a mayúsculas y quitar espacios en tiempo real
        input.value = input.value.toUpperCase().replace(/\s/g, '');
    }
});

document.addEventListener('focusout', function (e) {
    if (e.target.classList.contains('curp-input')) {
        const input = e.target;
        const valor = input.value.trim();
        // Buscar el mensaje de error que está justo después o en el mismo contenedor
        const errorMsg = input.parentElement.querySelector('.error-curp');

        if (valor === "") {
            input.classList.remove('is-invalid', 'is-valid');
            if (errorMsg) errorMsg.style.display = 'none';
            return;
        }

        if (!regexCurp.test(valor)) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
            if (errorMsg) {
                errorMsg.textContent = "CURP inválido (formato oficial).";
                errorMsg.style.display = 'block';
            }
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            if (errorMsg) errorMsg.style.display = 'none';
        }
    }
});

    // ==========================================
    // 4. EDAD VS NIVEL
    // ==========================================
    function obtenerEdad(fechaNacimiento) {
        if (!fechaNacimiento) return 0;
        const hoy = new Date();
        const cumple = new Date(fechaNacimiento);
        let edad = hoy.getFullYear() - cumple.getFullYear();
        const mes = hoy.getMonth() - cumple.getMonth();
        if (mes < 0 || (mes === 0 && hoy.getDate() < cumple.getDate())) edad--;
        return edad;
    }

    const validarEdadNivel = () => {
        if (!inputFecha || !selectNivel) return true;
        const fecha = inputFecha.value;
        const nivel = parseInt(selectNivel.value);
        if (!fecha || !nivel || isNaN(nivel)) return true;

        const edad = obtenerEdad(fecha);
        let errorEdad = "";
        let esBloqueante = true; 

        switch (nivel) {
            case 1: if (edad < 3 || edad > 6) errorEdad = "Edad para Kinder: 3-6 años."; break;
            case 2: if (edad < 6 || edad > 15) errorEdad = "Edad para Primaria: 6-15 años."; break;
            case 3: if (edad < 11 || edad > 18) errorEdad = "Edad para Secundaria: 11-18 años."; break;
            case 4: if (edad < 14 || edad > 25) errorEdad = "Edad para Prepa: 14-25 años."; break;
            case 5: if (edad < 16) { errorEdad = "Universidad: Mínimo 16 años."; esBloqueante = false; } break;
        }

        if (errorEdad) {
            if (mensajeErrorEdad) {
                mensajeErrorEdad.textContent = "⚠️ " + errorEdad;
                mensajeErrorEdad.style.display = 'block';
            }
            inputFecha.classList.add(esBloqueante ? 'is-invalid' : 'is-warning');
            inputFecha.dataset.invalid = esBloqueante ? "true" : "false";
            return !esBloqueante;
        } else {
            if (mensajeErrorEdad) mensajeErrorEdad.style.display = 'none';
            inputFecha.classList.remove('is-invalid', 'is-warning');
            inputFecha.classList.add('is-valid');
            inputFecha.dataset.invalid = "false";
            return true;
        }
    };

    if (inputFecha && selectNivel) {
        inputFecha.addEventListener('change', validarEdadNivel);
        selectNivel.addEventListener('change', validarEdadNivel);
    }

    // ==========================================
    // 5. TELÉFONOS (10 DÍGITOS)
    // ==========================================
    camposTelefono.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
        input.addEventListener('blur', function() {
            const valor = this.value.trim();
            if (valor === "" && !this.required) {
                this.classList.remove('is-invalid', 'is-valid');
                return;
            }
            if (valor.length !== 10) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

    // ==========================================
// 6. BLOQUEO DE ENVÍO (ÚNICO Y UNIFICADO)
// ==========================================
if (formularioAlumno) {
    formularioAlumno.addEventListener('submit', function(e) {
        // 1. Ejecutamos validaciones manuales antes de checar clases
        validarEdadNivel(); 
        
        // 2. Verificamos si hay algún campo con la clase 'is-invalid'
        const boletaInvalida = inputBoleta && inputBoleta.classList.contains('is-invalid');
        const edadInvalida   = inputFecha && inputFecha.dataset.invalid === "true";
        
        // Buscamos si CUALQUIER input de CURP tiene error
        const curpsInvalidos = Array.from(document.querySelectorAll('.curp-input'))
                                    .some(input => input.classList.contains('is-invalid'));
        
        // Buscamos si CUALQUIER teléfono tiene error
        const telInvalido    = Array.from(camposTelefono)
                                    .some(t => t.classList.contains('is-invalid'));

        // 3. Si algo está mal, frenamos el envío
        if (boletaInvalida || edadInvalida || curpsInvalidos || telInvalido) {
            e.preventDefault(); // Detiene el envío del formulario
            
            alert("❌ No se puede guardar. Revisa los campos en rojo:\n- Boleta\n- CURP\n- Teléfono\n- Fecha de Nacimiento");
            
            // Hacer scroll y foco al primer error encontrado para ayudar al usuario
            const primerError = document.querySelector('.is-invalid');
            if (primerError) {
                primerError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                primerError.focus();
            }
        }
    });
}

    // ==========================================
    // 7. OTROS (MODAL TUTOR, BAJA, DOCUMENTOS)
    // ==========================================
    // Tutor Dinámico
    if (selectNivel && selectTutor) {
        function actualizarTutor() {
            const nivelId = parseInt(selectNivel.value);
            const labelTutor = selectTutor.closest('.row').querySelector('label');
            if (nivelId >= 1 && nivelId <= 3) {
                selectTutor.required = true;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado *";
            } else {
                selectTutor.required = false;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado (Opcional)";
            }
        }
        selectNivel.addEventListener('change', actualizarTutor);
    }

    // Modal Tutor AJAX
    const formTutorModal = document.getElementById('formNuevoTutor');
    if (formTutorModal) {
        formTutorModal.addEventListener('submit', function(e) {
            e.preventDefault();
            const curpTutor = this.querySelector('.curp-input');
        if (curpTutor && curpTutor.classList.contains('is-invalid')) {
            alert(" CURP del tutor inválido");
            curpTutor.focus();
            return; 
        }
            const apiUrl = this.getAttribute('data-api-url');
            const formData = new FormData(this);
            fetch(apiUrl, { 
                method: 'POST', 
                body: formData, 
                headers: { 'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    bootstrap.Modal.getInstance(document.getElementById('modalNuevoTutor')).hide();
                    const opt = new Option(data.tutor_nombre, data.tutor_id);
                    selectTutor.add(opt);
                    selectTutor.value = data.tutor_id;
                    alert('Tutor registrado.');
                }
            });
        });
    }

    // Botones de Documentos
    const btnVis = document.getElementById('btnVisualizarDoc');
    const btnDes = document.getElementById('btnDescargarDoc');
    const selDoc = document.getElementById('selectDocumento');
    if (btnVis) {
        btnVis.addEventListener('click', () => {
            if(!selDoc.value) return alert('Elija un documento');
            window.open(`${btnVis.dataset.url}?tipo=${selDoc.value}`, '_blank');
        });
    }
});