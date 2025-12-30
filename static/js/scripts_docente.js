document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // 1. MODAL DESASIGNAR
    // ==========================================
    var modalDesasignar = document.getElementById('modalDesasignar');
    
    if (modalDesasignar) {
        modalDesasignar.addEventListener('show.bs.modal', function (event) {
            // Botón que activó el modal
            var button = event.relatedTarget;
            
            // Extraer info de los atributos data-
            var idGrupo = button.getAttribute('data-grupo-id');
            var nombreGrupo = button.getAttribute('data-grupo-nombre');
            
            // Actualizar el contenido del modal
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
        
        // Verificamos que se haya seleccionado algo válido
        if (!tipo || tipo === "Seleccione una opción") {
            alert('Por favor, seleccione un tipo de documento.');
            return;
        }

        // Obtenemos la URL base desde el atributo del botón
        const baseUrl = btnVisualizar.getAttribute('data-url');
        
        // Construimos la URL final
        let finalUrl = `${baseUrl}?tipo=${tipo}`;
        if (downloadMode) { finalUrl += '&download=true'; }

        // Abrir en nueva pestaña
        window.open(finalUrl, '_blank');
    }

    if (btnVisualizar && selectDoc) {
        btnVisualizar.addEventListener('click', function() {
            abrirDocumentoDocente(false);
        });
    }

    if (btnDescargar && selectDoc) {
        btnDescargar.addEventListener('click', function() {
            abrirDocumentoDocente(true);
        });
    }

    // ==========================================
    // 3. IMPRIMIR FICHA TECNICA
    // ==========================================
    const btnFicha = document.getElementById('btnImprimirFichaDocente');

    if (btnFicha) {
        btnFicha.addEventListener('click', function() {
            const baseUrl = this.getAttribute('data-url');
            // Abrimos directamente el tipo 'ficha'
            window.open(`${baseUrl}?tipo=ficha`, '_blank');
        });
    }

});