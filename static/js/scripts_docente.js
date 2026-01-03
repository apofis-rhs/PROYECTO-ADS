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

}); // Fin DOMContentLoaded