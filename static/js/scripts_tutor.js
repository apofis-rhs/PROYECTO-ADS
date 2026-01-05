document.addEventListener('DOMContentLoaded', function() {
    
    // --- Select de Hijos ---
    var selectHijo = document.getElementById('selectHijo');
    if (selectHijo) {
        selectHijo.addEventListener('change', function() {
            var idHijo = this.value;
            if (idHijo) {
                window.location.href = '?id_hijo=' + idHijo;
            }
        });
    }

    // --- Boton para imprimir ficha del tutor ---
    const btnFicha = document.getElementById('btnImprimirFichaTutor');
    
    if (btnFicha) {
        btnFicha.addEventListener('click', function() {
            const baseUrl = this.getAttribute('data-url');
            if (baseUrl) {
                // Abrimos el PDF en una nueva pestaña
                window.open(`${baseUrl}?tipo=ficha`, '_blank');
            } else {
                console.error("Error: URL no encontrada en el botón.");
            }
        });
    }
});