
document.addEventListener('DOMContentLoaded', function() {
    console.log("Script de docente cargado y operativo.");

    // ==========================================
    // 1. MODAL DESASIGNAR
    // ==========================================
    var modalDesasignar = document.getElementById('modalDesasignar');
    if (modalDesasignar) {
        modalDesasignar.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var idGrupo = button.getAttribute('data-grupo-id');
            var nombreGrupo = button.getAttribute('data-grupo-nombre');
            var modalTitle = modalDesasignar.querySelector('#nombreMateriaModal');
            var inputId = modalDesasignar.querySelector('#inputGrupoId');
            modalTitle.textContent = nombreGrupo;
            inputId.value = idGrupo;
        });
    }

    // ==========================================
    // 2. GENERACIÓN PDF DOCENTE
    // ==========================================
    const btnVisualizar = document.getElementById('btnVisualizarDocente');
    const btnDescargar = document.getElementById('btnDescargarDocente');
    const selectDoc = document.getElementById('selectDocumentoDocente');

    function abrirDocumentoDocente(downloadMode) {
        const tipo = selectDoc.value;
        if (!tipo || tipo === "Seleccione una opción") {
            alert('Por favor, seleccione un tipo de documento.');
            return;
        }
        const baseUrl = btnVisualizar.getAttribute('data-url');
        let finalUrl = `${baseUrl}?tipo=${tipo}`;
        if (downloadMode) { finalUrl += '&download=true'; }
        window.open(finalUrl, '_blank');
    }

    if (btnVisualizar && selectDoc) {
        btnVisualizar.addEventListener('click', () => abrirDocumentoDocente(false));
    }
    if (btnDescargar && selectDoc) {
        btnDescargar.addEventListener('click', () => abrirDocumentoDocente(true));
    }

    // ==========================================
    // 3. IMPRIMIR FICHA TÉCNICA
    // ==========================================
    const btnFicha = document.getElementById('btnImprimirFichaDocente');
    if (btnFicha) {
        btnFicha.addEventListener('click', function() {
            const baseUrl = this.getAttribute('data-url');
            window.open(`${baseUrl}?tipo=ficha`, '_blank');
        });
    }

    // ==========================================
// 4. VALIDACIÓN DE TELÉFONOS 
// ==========================================
const camposTelefono = document.querySelectorAll('input[name*="telefono"]');

camposTelefono.forEach(input => {

    // Bloquear letras y símbolos
    input.addEventListener('keydown', function(e) {
        const teclasPermitidas = [
            'Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'
        ];

        if (teclasPermitidas.includes(e.key)) return;

        // Solo números
        if (!/^\d$/.test(e.key)) {
            e.preventDefault();
        }
    });

    // Limpieza extra 
    input.addEventListener('input', function() {
        this.value = this.value.replace(/\D/g, '');
    });

    // Validar longitud
    input.addEventListener('blur', function() {
        const valor = this.value.trim();
        if (valor === "") {
            this.classList.remove('is-invalid', 'is-valid');
            return;
        }
        if (valor.length !== 10) {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
});

// ==========================================
    // 5. VALIDACIÓN DE CURP Y RFC
    // ==========================================
    
    const aplicarValidacionDoc = (nombreCampo, regex) => {
    const input = document.querySelector(`input[name="${nombreCampo}"]`);
    if (!input) return;

    // Mayúsculas y sin espacios
    input.addEventListener('input', function() {
        this.value = this.value.toUpperCase().replace(/\s/g, '');
    });

    input.addEventListener('blur', function() {
        const valor = this.value.trim();

        // Campo obligatorio
        if (valor === "") {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
            return;
        }

        if (!regex.test(valor)) {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
};


    // Regex oficiales
    const regexCURP = /^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM]([A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$/;
    const regexRFC = /^[A-ZÑ&]{3,4}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[A-Z\d]{3}$/;

    // Ejecutamos la función
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
// 7. LÓGICA PARA LIMPIAR FOTO (FINAL)
// ==========================================
document.addEventListener('click', function (e) {

    if (e.target && e.target.id === 'btnLimpiarFoto') {

        const contenedor = e.target.closest('.input-group');

        // Reemplazamos TODO el input-group
        contenedor.innerHTML = `
            <input type="file" class="form-control" name="foto" id="foto">
            <button type="button" class="btn btn-danger" id="btnLimpiarFoto">X</button>
        `;

      
    }
});


// ==========================================
// 8. PERSISTENCIA DE DATOS (Auto-guardado Docente)
// ==========================================
const camposDocente = document.querySelectorAll('form input:not([type="file"]), form select, form textarea');

// 1. Restaurar datos al cargar
camposDocente.forEach(campo => {
    // Usamos un prefijo único 'docente_' para no mezclar con los datos de alumnos
    const valorGuardado = localStorage.getItem('form_docente_' + campo.name);
    
    if (valorGuardado && valorGuardado !== "undefined") {
        campo.value = valorGuardado;
        
        // Disparar eventos por si hay lógica dependiente (ej. estados/municipios)
        campo.dispatchEvent(new Event('change'));
        campo.dispatchEvent(new Event('blur')); 
    }
});

// 2. Guardar cambios en tiempo real
camposDocente.forEach(campo => {
    campo.addEventListener('input', () => {
        // No guardamos si el campo es de tipo password por seguridad
        if (campo.type !== 'password') {
            localStorage.setItem('form_docente_' + campo.name, campo.value);
        }
    });
});

// 3. Limpiar al enviar el formulario con éxito
const formDocente = document.querySelector('form'); // Ajusta el selector si tienes ID
if (formDocente) {
    formDocente.addEventListener('submit', (e) => {
        const errores = formDocente.querySelectorAll('.is-invalid');
        if (errores.length === 0) {
            camposDocente.forEach(campo => {
                localStorage.removeItem('form_docente_' + campo.name);
            });
        }
    });
}
        // ==========================================
    // 9. VALIDACIÓN Y MÁSCARA NÚMERO DE EMPLEADO (DOC-AAAA-###)
    // ==========================================
    const inputEmpleado = document.getElementById('num_empleado');
    const mensajeErrorEmpleado = document.getElementById('errorEmpleado');

    if (inputEmpleado) {
        inputEmpleado.addEventListener('input', function(e) {
            // 1. Limpiar el valor: solo letras y números, y pasar a Mayúsculas
            let v = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
            
            // 2. Aplicar la máscara DOC-AAAA-###
            let maskedValue = "";
            
            // Si empieza con algo que no es DOC, forzamos que empiece con DOC
            if (v.length > 0 && !v.startsWith("DOC")) {
                v = "DOC" + v;
            }

            if (v.length > 0) {
                maskedValue = v.substring(0, 3); // DOC
                if (v.length > 3) {
                    maskedValue += "-" + v.substring(3, 7); // DOC-2024
                }
                if (v.length > 7) {
                    maskedValue += "-" + v.substring(7, 10); // DOC-2024-001
                }
            }
            
            this.value = maskedValue;
            this.classList.remove('is-invalid');
            if (mensajeErrorEmpleado) mensajeErrorEmpleado.style.display = 'none';
        });

        inputEmpleado.addEventListener('blur', function() {
            const valor = this.value.trim();
            const añoActual = new Date().getFullYear();
            const regexEmpleado = /^DOC-\d{4}-\d{3}$/;
            
            this.classList.remove('is-invalid', 'is-valid');

            if (valor !== "") {
                if (!regexEmpleado.test(valor)) {
                    this.classList.add('is-invalid');
                    if (mensajeErrorEmpleado) {
                        mensajeErrorEmpleado.textContent = "Formato inválido. Use: DOC-AAAA-###";
                        mensajeErrorEmpleado.style.display = 'block';
                    }
                } else {
                    // Validar año de ingreso
                    const partes = valor.split('-');
                    const añoIngreso = parseInt(partes[1]);
                    
                    if (añoIngreso > añoActual) {
                        this.classList.add('is-invalid');
                        if (mensajeErrorEmpleado) {
                            mensajeErrorEmpleado.textContent = `El año (${añoIngreso}) no puede ser mayor al actual.`;
                            mensajeErrorEmpleado.style.display = 'block';
                        }
                    } else {
                        this.classList.add('is-valid');
                    }
                }
            }
        });
    }

    // ==========================================
    // 10. VALIDACIÓN DE EDAD MÍNIMA (DOCENTE)
    // ==========================================
    const inputFechaNac = document.getElementById('fecha_nacimiento');
    const mensajeErrorFecha = document.getElementById('errorFecha');

    if (inputFechaNac) {
        inputFechaNac.addEventListener('blur', function() {
            const fechaSeleccionada = new Date(this.value);
            const hoy = new Date();
            
            // Calculamos la edad
            let edad = hoy.getFullYear() - fechaSeleccionada.getFullYear();
            const mes = hoy.getMonth() - fechaSeleccionada.getMonth();
            
            // Ajuste por si aún no ha cumplido años este año
            if (mes < 0 || (mes === 0 && hoy.getDate() < fechaSeleccionada.getDate())) {
                edad--;
            }

            this.classList.remove('is-invalid', 'is-valid');
            if (mensajeErrorFecha) mensajeErrorFecha.style.display = 'none';

            if (this.value !== "") {
                if (edad < 24) {
                    // Si es menor de 24 años
                    this.classList.add('is-invalid');
                    if (mensajeErrorFecha) {
                        mensajeErrorFecha.textContent = `Fecha no válida: El docente debe tener al menos 24 años.`;
                        mensajeErrorFecha.style.display = 'block';
                    }
                } else if (edad > 75) {
                    // Opcional: Validación por si ponen un año como 1920
                    this.classList.add('is-invalid');
                    if (mensajeErrorFecha) {
                        mensajeErrorFecha.textContent = "Fecha no válida: La edad excede el límite de jubilación.";
                        mensajeErrorFecha.style.display = 'block';
                    }
                } else {
                    this.classList.add('is-valid');
                }
            }
        });
    }


}); // Fin DOMContentLoaded

