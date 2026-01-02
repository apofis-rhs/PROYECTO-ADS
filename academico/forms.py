# academico/forms.py
from django import forms
from .models import Materia, Grupo

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = [
            "clave",
            "nombre",
            "creditos",
            "nivel_sugerido",
            "carrera",
            "nivel_educativo",
            "sesiones_por_semana",
        ]


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = [
            "nivel",        # primero seleccionamos nivel
            "materia",      # luego la materia
            "clave_grupo",
            "grado",
            "periodo",
            "turno",
            # OJO: no incluimos 'docente' aqui
        ]

