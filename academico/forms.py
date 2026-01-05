# academico/forms.py
from django import forms
from .models import Materia, Grupo
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

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

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)