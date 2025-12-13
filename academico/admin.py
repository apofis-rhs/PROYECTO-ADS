from django.contrib import admin
from .models import Alumno, Docente, PadreTutor, NivelEducativo, CatTipoRelacionTutor

# Config para ver el Nivel Educativo
class NivelEducativoAdmin(admin.ModelAdmin):
    list_display = ('id_nivel', 'nombre')

# Config para ver el Tipo de Relación
class CatTipoRelacionTutorAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_relacion', 'nombre')

# Config para ver Alumnos
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('boleta', 'nombre', 'ape_paterno', 'ape_materno', 'curp', 'nivel')
    search_fields = ('boleta', 'nombre', 'ape_paterno', 'curp')
    # Filtros laterales
    list_filter = ('nivel', 'sexo')

# Config para ver Docentes
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('num_empleado', 'nombre', 'ape_paterno', 'rfc', 'activo')
    search_fields = ('num_empleado', 'nombre', 'ape_paterno', 'rfc')
    list_filter = ('activo', 'grado_academico')

# Config para ver Tutores
class PadreTutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ape_paterno', 'telefono', 'curp')
    search_fields = ('nombre', 'ape_paterno', 'curp')

# Registramos los modelos
admin.site.register(NivelEducativo, NivelEducativoAdmin)
admin.site.register(CatTipoRelacionTutor, CatTipoRelacionTutorAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(PadreTutor, PadreTutorAdmin)