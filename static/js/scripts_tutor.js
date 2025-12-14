document.addEventListener('DOMContentLoaded', function() {
    
    // Referencia al select de hijos en visualizar_tutor.html
    var selectHijo = document.getElementById('selectHijo');

    if (selectHijo) {
        selectHijo.addEventListener('change', function() {
            var idHijo = this.value;
            
            // Recargamos la página enviando el ID del hijo como parámetro GET
            // Esto hará que la vista de Django procese y muestre los datos de ese alumno
            if (idHijo) {
                window.location.href = '?id_hijo=' + idHijo;
            }
        });
    }
});