document.addEventListener('DOMContentLoaded', function() {
    console.log("JS de Alumno cargado y operativo.");

    // ==========================================
    // 1. SELECTORES GLOBALES
    // ==========================================
    const formularioAlumno = document.querySelector('form:not(#formNuevoTutor)');
    const inputBoleta = document.querySelector('input[name="boleta"]');
    const mensajeErrorBoleta = document.getElementById('errorBoleta');
    const selectNivel = document.querySelector('select[name="nivel"]');

    const selectGrado = document.getElementById('selectGrado'); // Añadido


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
        
        // 1. SIEMPRE LIMPIAMOS TODO AL SALIR
        this.classList.remove('is-invalid', 'is-valid');
        if (mensajeErrorBoleta) {
            mensajeErrorBoleta.style.display = 'none';
        }

        // 2. SOLO VALIDAMOS SI EL CAMPO NO ESTÁ VACÍO
        if (valor !== "") {
            if (!regexBoleta.test(valor)) {
                // Formato incorrecto
                this.classList.add('is-invalid');
                if (mensajeErrorBoleta) {
                    mensajeErrorBoleta.textContent = "Formato inválido: Año(4) + 430 + 3 dígitos.";
                    mensajeErrorBoleta.style.display = 'block';
                }
            } else {
                const añoIngreso = parseInt(valor.substring(0, 4));
                if (añoIngreso > añoActual) {
                    // Año futuro
                    this.classList.add('is-invalid');
                    if (mensajeErrorBoleta) {
                        mensajeErrorBoleta.textContent = `El año (${añoIngreso}) no puede ser mayor al actual.`;
                        mensajeErrorBoleta.style.display = 'block';
                    }
                } else {
                    // TODO CORRECTO
                    this.classList.add('is-valid');
                }
            }
        } 
        // Si valor === "", no entra al IF y el campo se queda limpio (sin clases)
    });

    // Opcional: Quitar el error mientras el usuario está corrigiendo (mejora la UX)
    inputBoleta.addEventListener('input', function() {
        this.classList.remove('is-invalid');
    });
}
  
// ==========================================
// 5. VALIDACIÓN DE CURP Y RFC (OPTIMIZADO)
// ==========================================

const aplicarValidacionDoc = (nombreCampo, regex) => {
    const inputs = document.querySelectorAll(`input[name="${nombreCampo}"]`);
    if (inputs.length === 0) return;

    inputs.forEach(input => {
        // Mientras el usuario escribe
        input.addEventListener('input', function() {
            // Convertir a mayúsculas y quitar espacios
            this.value = this.value.toUpperCase().replace(/\s/g, '');
            
            // Quitar el rojo de error mientras edita
            this.classList.remove('is-invalid');

            // OPCIONAL: Si ya tiene la longitud completa y es válido, poner palomita de una vez
            const longitudRequerida = (nombreCampo === 'curp') ? 18 : 13;
            if (this.value.length >= longitudRequerida && regex.test(this.value)) {
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
            }
        });

        // Cuando el usuario sale del campo (Tab o Click fuera)
        input.addEventListener('blur', function() {
            const valor = this.value.trim();

            // 1. Limpieza total de estados antes de validar
            this.classList.remove('is-invalid', 'is-valid');

            // 2. Si el campo está vacío
            if (valor === "") {
                if (this.required) {
                    this.classList.add('is-invalid');
                }
                return; // Salimos sin poner palomita
            }

            // 3. Validación con la Regex
            if (regex.test(valor)) {
                // ÉXITO: Se pone borde verde y palomita
                this.classList.add('is-valid');
            } else {
                // ERROR: Se pone borde rojo y X
                this.classList.add('is-invalid');
            }
        });
    });
};

// Regex oficiales
const regexCURP = /^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM]([A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$/;
const regexRFC = /^[A-ZÑ&]{3,4}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[A-Z\d]{3}$/;

// Ejecución para todos los campos presentes en el HTML (Alumno y Tutor)
aplicarValidacionDoc('curp', regexCURP);
aplicarValidacionDoc('rfc', regexRFC);


    // ==========================================
    // 6. BLOQUEO DE ENVÍO SI HAY ERRORES
    // ==========================================
    const formulario = document.querySelector('form');
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            const errores = this.querySelectorAll('.is-invalid');
            if (errores.length > 0) {
                e.preventDefault();
                alert("❌ Por favor, corrija los campos marcados en rojo (CURP, RFC o Teléfono) antes de guardar.");
                errores[0].focus();
            }
        });
    }


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
    // 6. LÓGICA DE NIVEL (GRADOS, TUTOR Y CORREO)
    // ==========================================
    if (selectNivel) {
        selectNivel.addEventListener('change', function() {
            const nivelId = this.value;
            
            // A. Grados Dinámicos
            selectGrado.innerHTML = '<option value="">Seleccionar...</option>';
            let opciones = [];
            switch (nivelId) {
                case "1": opciones = ["1° Kinder", "2° Kinder", "3° Kinder"]; break;
                case "2": opciones = ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"]; break;
                case "3": opciones = ["1° Secundaria", "2° Secundaria", "3° Secundaria"]; break;
                case "4": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre"]; break;
                case "5": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre", "7° Semestre", "8° Semestre"]; break;
            }
            opciones.forEach(grado => {
                const opt = new Option(grado, grado); // Corregido: value ahora es el texto completo
                selectGrado.add(opt);
            });

            // B. Tutor y Correo Dinámico
            const labelTutor = selectTutor.closest('.col-8').querySelector('label');
            if (["1", "2", "3"].includes(nivelId)) {
                // Básica
                selectTutor.required = true;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado * <small class='text-muted'>(Obligatorio)</small>";
                if(contenedorCorreo) contenedorCorreo.style.display = 'none';
                if(inputCorreo) { inputCorreo.required = false; inputCorreo.value = ""; }
            } else {
                // Superior
                selectTutor.required = false;
                if(labelTutor) labelTutor.innerHTML = "Tutor Asignado <small class='text-muted'>(Opcional)</small>";
                if(contenedorCorreo) contenedorCorreo.style.display = 'block';
                if(inputCorreo) inputCorreo.required = true;
            }
        });
    }


    // ==========================================
// 7. BLOQUEO DE ENVÍO (ÚNICO Y UNIFICADO)
// ==========================================
if (formularioAlumno) {
        formularioAlumno.addEventListener('submit', function(e) {
            const nivelId = selectNivel.value;
            
            // Si es Prepa (4) o Universidad (5), validamos el correo del alumno forzosamente
            if (["4", "5"].includes(nivelId)) {
                if (inputCorreo) {
                    validarEmail(inputCorreo);
                }
            }

            // Validamos que el Tutor esté seleccionado si es nivel básico
            if (["1", "2", "3"].includes(nivelId)) {
                if (!selectTutor.value) {
                    selectTutor.classList.add('is-invalid');
                } else {
                    selectTutor.classList.remove('is-invalid');
                }
            }

            // Checamos si hay CUALQUIER error en el formulario
            const errores = document.querySelectorAll('.is-invalid');
            
            if (errores.length > 0) {
                e.preventDefault();
                alert(" No se puede guardar. Hay campos obligatorios vacíos o con errores (CURP, Teléfono, Correo o Boleta).");
                
                // Scroll al primer error
                errores[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                errores[0].focus();
            }
        });
    }

    // ==========================================
    // 8. OTROS (MODAL TUTOR, BAJA, DOCUMENTOS)
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

    // ==========================================
// 9. GRADOS Y SEMESTRES DINÁMICOS
// ==========================================

if (selectNivel && selectGrado) {
    selectNivel.addEventListener('change', function() {
        const nivelId = this.value; // El ID del nivel seleccionado
        
        // Limpiar opciones anteriores
        selectGrado.innerHTML = '<option value="">Seleccionar...</option>';
        
        let opciones = [];

        // Definimos grados según el ID del nivel
        // Ajusta los números (1, 2, 3...) según tus IDs de la base de datos
        switch (nivelId) {
            case "1": // Kinder
                opciones = ["1° Kinder", "2° Kinder", "3° Kinder"];
                break;
            case "2": // Primaria   
                opciones = ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"];
                break;
            case "3": // Secundaria
                opciones = ["1° Secundaria", "2° Secundaria", "3° Secundaria"];
                break;
            case "4": // Preparatoria
                opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre"];
                break;
            case "5": // Universidad
                opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre", "7° Semestre", "8° Semestre", "9° Semestre", "10° Semestre"];
                break;
        }

        // Agregar las nuevas opciones al select
        opciones.forEach(grado => {
            const opt = document.createElement('option');
            opt.value = grado[0];
            opt.textContent = grado;
            selectGrado.appendChild(opt);
        });
    });
}

// ==========================================
    // 10. VALIDACIÓN DE CORREOS OBLIGATORIOS
    // ==========================================
    const regexCorreo = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    const validarEmail = (input) => {
        const valor = input.value.trim();
        input.classList.remove('is-invalid', 'is-valid');

        // 1. Validar que no esté vacío (Obligatorio)
        if (valor === "") {
            input.classList.add('is-invalid');
            return false;
        }

        // 2. Validar formato con Regex
        if (regexCorreo.test(valor)) {
            input.classList.add('is-valid');
            return true;
        } else {
            input.classList.add('is-invalid');
            return false;
        }
    };

    // Aplicar a todos los campos de email
    const camposCorreo = document.querySelectorAll('input[type="email"]');
    camposCorreo.forEach(input => {
        // Validar al salir del campo
        input.addEventListener('blur', function() {
            validarEmail(this);
        });
        
        // Limpiar error mientras el usuario corrige
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        });
    });

    
});

//tache para eliminar documento adjunto

    function limpiarFoto() {
    document.getElementById("foto").value = "";
  }

  // ==========================================
// 10. PERSISTENCIA DE DATOS (Auto-guardado)
// ==========================================
const camposAPersistir = document.querySelectorAll('input:not([type="file"]), select');

// 1. Restaurar los datos al cargar la página
camposAPersistir.forEach(campo => {
    const valorGuardado = localStorage.getItem('form_alumno_' + campo.name);
    if (valorGuardado) {
        campo.value = valorGuardado;
        // Disparar evento change para que se activen tus validaciones y lógica dinámica
        campo.dispatchEvent(new Event('change'));
    }
});

// 2. Guardar los datos cada vez que el usuario escriba o cambie algo
camposAPersistir.forEach(campo => {
    campo.addEventListener('input', () => {
        localStorage.setItem('form_alumno_' + campo.name, campo.value);
    });
});

// 3. Limpiar el localStorage solo cuando el formulario se envíe con éxito
if (formularioAlumno) {
    formularioAlumno.addEventListener('submit', (e) => {
        // Solo si no hay errores (is-invalid), procedemos a limpiar
        const errores = document.querySelectorAll('.is-invalid');
        if (errores.length === 0) {
            camposAPersistir.forEach(campo => {
                localStorage.removeItem('form_alumno_' + campo.name);
            });
        }
    });
}