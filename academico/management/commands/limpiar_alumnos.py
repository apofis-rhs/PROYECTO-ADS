from django.core.management.base import BaseCommand
from django.utils import timezone
from academico.models import Alumno

class Command(BaseCommand):
    help = 'Elimina definitivamente a los alumnos cuya fecha de baja expiró hace 30 días'

    def handle(self, *args, **kwargs):
        hoy = timezone.now()
        
        # Buscamos alumnos cuya fecha de eliminación sea HOY o ANTES de hoy
        alumnos_a_borrar = Alumno.objects.filter(
            fecha_eliminacion__lte=hoy,
            activo=False
        )
        
        cantidad = alumnos_a_borrar.count()
        
        if cantidad > 0:
            self.stdout.write(self.style.WARNING(f'Se encontraron {cantidad} alumnos para borrar...'))
            
            # Aquí ocurre el borrado real de la base de datos
            alumnos_a_borrar.delete()
            
            self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se eliminaron {cantidad} registros permanentemente.'))
        else:
            self.stdout.write(self.style.SUCCESS('No hay alumnos pendientes de eliminación hoy.'))