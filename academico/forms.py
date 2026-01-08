# academico/forms.py
from django import forms
from .models import Materia, Grupo
# ----------------------------------
# ULTIMA MODIFIACION EM CASO QUE ALGO NO FUNCIONE 
from django.core.exceptions import ValidationError
from .models import Horario  # asegúrate de importar Horario


def clean_docente(self):
    docente = self.cleaned_data.get("docente")

    # Docente es opcional
    if not docente:
        return docente

    # Si es creación, todavía no hay horarios del grupo; la validación dura se hace en el generador.
    if not getattr(self.instance, "pk", None):
        return docente

    grupo_id = self.instance.id_grupo

    # Horarios del grupo actual
    horarios_grupo = list(Horario.objects.filter(grupo_id=grupo_id).only("dia_semana", "hora_inicio", "hora_fin"))
    if not horarios_grupo:
        return docente

    # Periodo del grupo (si en el form lo cambias, toma el nuevo; si no, usa el actual)
    periodo = (self.cleaned_data.get("periodo") or getattr(self.instance, "periodo", None))

    # Horarios de otros grupos del mismo docente en el mismo periodo
    otros = (
        Horario.objects
        .select_related("grupo")
        .filter(grupo__periodo=periodo, grupo__docente_id=docente.id_docente)
        .exclude(grupo_id=grupo_id)
        .only("dia_semana", "hora_inicio", "hora_fin", "grupo__clave_grupo")
    )

    def traslapa(a_ini, a_fin, b_ini, b_fin):
        return (a_ini < b_fin) and (a_fin > b_ini)

    choques = []
    for hg in horarios_grupo:
        for ho in otros:
            if hg.dia_semana != ho.dia_semana:
                continue
            if traslapa(hg.hora_inicio, hg.hora_fin, ho.hora_inicio, ho.hora_fin):
                choques.append(
                    f"Día {hg.dia_semana}: {hg.hora_inicio.strftime('%H:%M')}-{hg.hora_fin.strftime('%H:%M')} "
                    f"choca con grupo {ho.grupo.clave_grupo} "
                    f"({ho.hora_inicio.strftime('%H:%M')}-{ho.hora_fin.strftime('%H:%M')})"
                )

    if choques:
        raise ValidationError(
            "No se puede asignar este docente porque tiene choques de horario:\n- " + "\n- ".join(choques)
        )

    return docente
# ---------------------------------- FIN DE LA ULTIMA

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
        
    from django.core.exceptions import ValidationError
    from .models import Horario  # asegúrate de importar Horario


    def clean_docente(self):
        docente = self.cleaned_data.get("docente")

        # Docente es opcional
        if not docente:
            return docente

        # Si es creación, todavía no hay horarios del grupo; la validación dura se hace en el generador.
        if not getattr(self.instance, "pk", None):
            return docente

        grupo_id = self.instance.id_grupo

        # Horarios del grupo actual
        horarios_grupo = list(Horario.objects.filter(grupo_id=grupo_id).only("dia_semana", "hora_inicio", "hora_fin"))
        if not horarios_grupo:
            return docente

        # Periodo del grupo (si en el form lo cambias, toma el nuevo; si no, usa el actual)
        periodo = (self.cleaned_data.get("periodo") or getattr(self.instance, "periodo", None))

        # Horarios de otros grupos del mismo docente en el mismo periodo
        otros = (
            Horario.objects
            .select_related("grupo")
            .filter(grupo__periodo=periodo, grupo__docente_id=docente.id_docente)
            .exclude(grupo_id=grupo_id)
            .only("dia_semana", "hora_inicio", "hora_fin", "grupo__clave_grupo")
        )

        def traslapa(a_ini, a_fin, b_ini, b_fin):
            return (a_ini < b_fin) and (a_fin > b_ini)

        choques = []
        for hg in horarios_grupo:
            for ho in otros:
                if hg.dia_semana != ho.dia_semana:
                    continue
                if traslapa(hg.hora_inicio, hg.hora_fin, ho.hora_inicio, ho.hora_fin):
                    choques.append(
                        f"Día {hg.dia_semana}: {hg.hora_inicio.strftime('%H:%M')}-{hg.hora_fin.strftime('%H:%M')} "
                        f"choca con grupo {ho.grupo.clave_grupo} "
                        f"({ho.hora_inicio.strftime('%H:%M')}-{ho.hora_fin.strftime('%H:%M')})"
                    )

        if choques:
            raise ValidationError(
                "No se puede asignar este docente porque tiene choques de horario:\n- " + "\n- ".join(choques)
            )

        return docente
# ---------------------------------- FIN DE LA ULTIMA para validar docente no repetido
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

