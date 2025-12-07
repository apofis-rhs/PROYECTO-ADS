from django.contrib import admin
from .models import Alumno, Docente, PadreTutor, NivelEducativo, CatTipoRelacionTutor

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('boleta', 'nombre', 'ape_paterno', 'nivel', 'contacto_emergencia')
    search_fields = ('boleta', 'nombre', 'ape_paterno')
    list_filter = ('nivel',)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('num_empleado', 'nombre', 'especialidad', 'activo')
    search_fields = ('num_empleado', 'nombre')

admin.site.register(PadreTutor)
admin.site.register(NivelEducativo)
admin.site.register(CatTipoRelacionTutor)