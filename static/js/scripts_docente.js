document.addEventListener('DOMContentLoaded', function() {
    // Lógica para el Modal de Desasignar (Eliminar) Materia
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
});