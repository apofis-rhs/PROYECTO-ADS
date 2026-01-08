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

# academico/forms.py
from django import forms
from .models import Grupo, Materia, Docente  # asegúrate de tener Docente en models


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = [
            "nivel",
            "materia",
            "docente",     # <-- NUEVO
            "grado",
            "periodo",
            "clave_grupo",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) Materias filtradas por nivel
        self.fields["materia"].queryset = Materia.objects.none()

        nivel_id = None

        # POST/GET
        if self.data.get("nivel"):
            try:
                nivel_id = int(self.data.get("nivel"))
            except (TypeError, ValueError):
                nivel_id = None

        # initial
        if not nivel_id and self.initial.get("nivel"):
            try:
                nivel_id = int(self.initial.get("nivel"))
            except (TypeError, ValueError):
                nivel_id = None

        # instance
        if not nivel_id and getattr(self.instance, "pk", None) and getattr(self.instance, "nivel_id", None):
            nivel_id = self.instance.nivel_id

        if nivel_id:
            self.fields["materia"].queryset = (
                Materia.objects.filter(nivel_educativo_id=nivel_id).order_by("nombre")
            )

        # 2) Docentes (por ahora: todos). Si luego quieres filtrar por nivel/carrera, lo hacemos.
        self.fields["docente"].queryset = Docente.objects.all().order_by("ape_paterno", "ape_materno", "nombre")
        self.fields["docente"].required = False  # opcional, por si aún no asignas docente

