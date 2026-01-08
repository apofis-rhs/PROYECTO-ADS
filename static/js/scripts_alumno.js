document.addEventListener('DOMContentLoaded', function() {
    console.log("JS de Alumno cargado y operativo.");

    // ==========================================
    // 1. SELECTORES GLOBALES
    // ==========================================
    const formularioAlumno = document.querySelector('form:not(#formNuevoTutor):not(#formBaja)');
    
    const inputBoleta = document.querySelector('input[name="boleta"]');
    const mensajeErrorBoleta = document.getElementById('errorBoleta');
    const selectNivel = document.querySelector('select[name="nivel"]');
    const selectGrado = document.getElementById('selectGrado');
    const selectTutor = document.querySelector('select[name="tutor"]');
    const inputFecha = document.querySelector('input[name="fecha_nacimiento"]');
    const mensajeErrorEdad = document.getElementById('errorEdadNivel');
    const inputCurp = document.querySelector('input[name="curp"]');
    const mensajeErrorCurp = document.getElementById('errorCurp');
    const camposTelefono = document.querySelectorAll('input[name*="telefono"]');

    // Selectores para el Correo dinámico
    const contenedorCorreo = document.getElementById('contenedorCorreoAlumno');
    const inputCorreo = document.getElementById('inputCorreoAlumno');

    // ==========================================
    // 2. VALIDACIÓN DE BOLETA (AAAA430###)
    // ==========================================
    if (inputBoleta) {
        inputBoleta.addEventListener('blur', function() {
            const valor = this.value.trim();
            const añoActual = new Date().getFullYear();
            const regexBoleta = /^\d{4}430\d{3}$/;
            
            this.classList.remove('is-invalid', 'is-valid');
            if (mensajeErrorBoleta) mensajeErrorBoleta.style.display = 'none';

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
                        this.classList.add('is-valid');
                    }
                }
            } 
        });

        inputBoleta.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    }

    // ==========================================
    // 3. VALIDACIÓN DE CURP Y RFC
    // ==========================================
    const aplicarValidacionDoc = (nombreCampo, regex) => {
        const inputs = document.querySelectorAll(`input[name="${nombreCampo}"]`);
        if (inputs.length === 0) return;

        inputs.forEach(input => {
            input.addEventListener('input', function() {
                this.value = this.value.toUpperCase().replace(/\s/g, '');
                this.classList.remove('is-invalid');
                
                const longitudRequerida = (nombreCampo === 'curp') ? 18 : 13;
                if (this.value.length >= longitudRequerida && regex.test(this.value)) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                }
            });

            input.addEventListener('blur', function() {
                const valor = this.value.trim();
                this.classList.remove('is-invalid', 'is-valid');

                if (valor === "") {
                    if (this.required) this.classList.add('is-invalid');
                    return;
                }

                if (regex.test(valor)) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            });
        });
    };

    const regexCURP = /^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM]([A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$/;
    const regexRFC = /^[A-ZÑ&]{3,4}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[A-Z\d]{3}$/;

    aplicarValidacionDoc('curp', regexCURP);
    aplicarValidacionDoc('rfc', regexRFC);

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
            return !esBloqueante;
        } else {
            if (mensajeErrorEdad) mensajeErrorEdad.style.display = 'none';
            inputFecha.classList.remove('is-invalid', 'is-warning');
            inputFecha.classList.add('is-valid');
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
    // 6. LÓGICA DE NIVEL (GRADOS, TUTOR Y CORREO)
    // ==========================================
    if (selectNivel) {
        selectNivel.addEventListener('change', function() {
            const nivelId = this.value;
            
            // A. Grados Dinámicos
            if (selectGrado) {
                selectGrado.innerHTML = '<option value="">Seleccionar...</option>';
                let opciones = [];
                switch (nivelId) {
                    case "1": opciones = ["1° Kinder", "2° Kinder", "3° Kinder"]; break;
                    case "2": opciones = ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"]; break;
                    case "3": opciones = ["1° Secundaria", "2° Secundaria", "3° Secundaria"]; break;
                    case "4": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre"]; break;
                    case "5": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre", "7° Semestre", "8° Semestre", "9° Semestre", "10° Semestre"]; break;
                }
                opciones.forEach(grado => {
                    const opt = document.createElement('option');
                    opt.value = grado; // Usamos el texto completo como valor
                    opt.textContent = grado;
                    selectGrado.appendChild(opt);
                });
            }

            // B. Tutor y Correo Dinámico
            if (selectTutor) {
                const labelTutor = selectTutor.closest('.row') ? selectTutor.closest('.row').querySelector('label') : null;
                
                if (["1", "2", "3"].includes(nivelId)) {
                    // Básica
                    selectTutor.required = true;
                    if(labelTutor) labelTutor.innerHTML = "Tutor Asignado * <small class='text-muted'>(Obligatorio)</small>";
                    if(contenedorCorreo) contenedorCorreo.style.display = 'none';
                    if(inputCorreo) { inputCorreo.required = false; inputCorreo.value = ""; inputCorreo.classList.remove('is-invalid'); }
                } else {
                    // Superior
                    selectTutor.required = false;
                    if(labelTutor) labelTutor.innerHTML = "Tutor Asignado <small class='text-muted'>(Opcional)</small>";
                    if(contenedorCorreo) contenedorCorreo.style.display = 'block';
                    if(inputCorreo) inputCorreo.required = true;
                }
            }
        });
    }

    // ==========================================
    // 7. VALIDACIÓN DE CORREO (REGEX)
    // ==========================================
    const regexCorreo = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    const validarEmail = (input) => {
        const valor = input.value.trim();
        input.classList.remove('is-invalid', 'is-valid');

        if (valor === "") {
            input.classList.add('is-invalid');
            return false;
        }

        if (regexCorreo.test(valor)) {
            input.classList.add('is-valid');
            return true;
        } else {
            input.classList.add('is-invalid');
            return false;
        }
    };

    if (inputCorreo) {
        inputCorreo.addEventListener('blur', function() {
            validarEmail(this);
        });
        inputCorreo.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    }

    // ==========================================
    // 8. BLOQUEO DE ENVÍO (FORMULARIO ALTA/EDICIÓN)
    // ==========================================
    if (formularioAlumno) {
        formularioAlumno.addEventListener('submit', function(e) {
            const nivelId = selectNivel ? selectNivel.value : "";
            
            // Si es Prepa (4) o Universidad (5), validamos el correo
            if (["4", "5"].includes(nivelId)) {
                if (inputCorreo && !validarEmail(inputCorreo)) {
                    // Error en correo
                }
            }

            // Validamos Tutor obligatorio en básica
            if (["1", "2", "3"].includes(nivelId)) {
                if (selectTutor && !selectTutor.value) {
                    selectTutor.classList.add('is-invalid');
                } else if (selectTutor) {
                    selectTutor.classList.remove('is-invalid');
                }
            }

            // Revisión final de errores
            const errores = document.querySelectorAll('.is-invalid');
            
            if (errores.length > 0) {
                e.preventDefault();
                alert("❌ No se puede guardar. Hay campos obligatorios vacíos o con errores.");
                errores[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                errores[0].focus();
            } else {
                // Si todo está bien, limpiamos el localStorage
                const camposLimpiar = document.querySelectorAll('input:not([type="file"]), select');
                camposLimpiar.forEach(campo => {
                    localStorage.removeItem('form_alumno_' + campo.name);
                });
            }
        });
    }

    // ==========================================
    // 9. MODAL NUEVO TUTOR (AJAX)
    // ==========================================
    const formTutorModal = document.getElementById('formNuevoTutor');
    if (formTutorModal) {
        formTutorModal.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const curpTutor = this.querySelector('.curp-input'); 
            if (curpTutor && curpTutor.classList.contains('is-invalid')) {
                alert("⚠️ CURP del tutor inválido");
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
                    const modalElement = document.getElementById('modalNuevoTutor');
                    const modalInstance = bootstrap.Modal.getInstance(modalElement);
                    if (modalInstance) modalInstance.hide();
                    
                    if (selectTutor) {
                        const opt = new Option(data.tutor_nombre, data.tutor_id);
                        selectTutor.add(opt);
                        selectTutor.value = data.tutor_id;
                    }
                    
                    this.reset();
                    alert('✅ Tutor registrado correctamente.');
                } else {
                    alert('❌ Error al registrar tutor: ' + data.error);
                }
            })
            .catch(err => {
                console.error(err);
                alert('Error de conexión.');
            });
        });
    }

    // ==========================================
    // 10. GESTIÓN CENTRALIZADA DE DOCUMENTOS
    // ==========================================
    const btnVisualizar = document.getElementById('btnVisualizarDoc');
    const btnDescargar = document.getElementById('btnDescargarDoc');
    const btnFicha = document.getElementById('btnImprimirFicha');
    const selectDocumento = document.getElementById('selectDocumento');

    function gestionarAperturaDocumento(tipoAccion) {
        if (tipoAccion === 'ficha') {
            if (btnFicha) {
                const urlFicha = btnFicha.getAttribute('data-url');
                if (urlFicha) window.open(`${urlFicha}?tipo=ficha`, '_blank');
            }
            return;
        }

        if (!selectDocumento.value) {
            alert('⚠️ Por favor, selecciona un tipo de documento del listado.');
            selectDocumento.focus();
            return;
        }

        const baseUrl = btnVisualizar.getAttribute('data-url');
        let urlFinal = `${baseUrl}?tipo=${selectDocumento.value}`;

        if (tipoAccion === 'descargar') {
            urlFinal += '&download=true';
        }

        window.open(urlFinal, '_blank');
    }

    if (btnVisualizar) btnVisualizar.addEventListener('click', () => gestionarAperturaDocumento('ver'));
    if (btnDescargar) btnDescargar.addEventListener('click', () => gestionarAperturaDocumento('descargar'));
    if (btnFicha) btnFicha.addEventListener('click', () => gestionarAperturaDocumento('ficha'));


    // ==========================================
    // 11. PERSISTENCIA DE DATOS (Auto-guardado)
    // ==========================================
    // 🛑 CORRECCIÓN CRÍTICA: Excluimos radio buttons (:not([type="radio"])) para no corromper sus valores
    const camposAPersistir = document.querySelectorAll('input:not([type="file"]):not([type="radio"]):not([type="checkbox"]):not([readonly]), select:not([disabled])');

    // 1. Restaurar
    camposAPersistir.forEach(campo => {
        const valorGuardado = localStorage.getItem('form_alumno_' + campo.name);
        if (valorGuardado) {
            campo.value = valorGuardado;
            campo.dispatchEvent(new Event('change')); 
        }
    });

    // 2. Guardar
    camposAPersistir.forEach(campo => {
        campo.addEventListener('input', () => {
            localStorage.setItem('form_alumno_' + campo.name, campo.value);
        });
    });

    // ==========================================
    // 12. CONFIRMACIÓN DE BAJA (SELECTOR CORREGIDO)
    // ==========================================
    const formBaja = document.getElementById('formBaja');
    
    if (formBaja) {
        formBaja.addEventListener('submit', function(e) {
            e.preventDefault(); 
            
            // Usamos FormData para leer el valor REAL que se enviará
            const formData = new FormData(formBaja);
            const tipo = formData.get('tipoBaja'); 

            if (!tipo) {
                alert("⚠️ Por favor, selecciona un tipo de baja.");
                return;
            }

            let mensaje = "";

            if (tipo === 'definitiva') {
                mensaje = "⚠️ ¡ATENCIÓN: ACCIÓN IRREVERSIBLE! ⚠️\n\n" +
                          "Estás a punto de ELIMINAR PERMANENTEMENTE a este alumno.\n" +
                          "--------------------------------------------------\n" +
                          "❌ Se borrará su expediente completo.\n" +
                          "❌ Se perderá su historial académico.\n" +
                          "❌ Esta acción NO SE PUEDE DESHACER.\n" +
                          "--------------------------------------------------\n\n" +
                          "¿Estás completamente seguro?";
            } else {
                mensaje = "CONFIRMACIÓN DE BAJA TEMPORAL\n\n" +
                          "ℹ️ El alumno pasará a estado 'Inactivo'.\n" +
                          "✅ Sus datos se conservarán.\n" +
                          "✅ Podrás reactivarlo después.\n\n" +
                          "¿Deseas continuar?";
            }

            if (confirm(mensaje)) {
                this.submit();
            }
        });
    }

}); // FIN DEL DOMContentLoaded