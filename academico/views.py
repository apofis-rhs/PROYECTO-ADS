from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Vista del Dashboard Principal
def dashboard_view(request):
    return render(request, 'dashboard.html')

def consultar_alumno_view(request):
    return render(request, 'alumno/consultar_alumno.html')

def visualizar_alumno_view(request):
    # En el futuro, aquí recibiremos un ID (request, id_alumno)
    return render(request, 'alumno/visualizar_alumno.html')

def anadir_alumno_view(request):
    return render(request, 'alumno/anadir_alumno.html')

def baja_alumno_view(request):
    return render(request, 'alumno/baja_alumno.html')

def cambio_carrera_view(request):
    return render(request, 'alumno/cambio_carrera.html')

def consultar_docente_view(request):
    return render(request, 'docente/consultar_docente.html')

def visualizar_docente_view(request):
    return render(request, 'docente/visualizar_docente.html')

def asignar_materia_view(request):
    # NOTA: en el futuro cargaremos las materias disponibles y el horario del profe (nomas que quede integrado todo)
    return render(request, 'docente/asignar_materia.html')

def anadir_docente_view(request):
    return render(request, 'docente/anadir_docente.html')

def consultar_tutor_view(request):
    return render(request, 'tutor/consultar_tutor.html')

def visualizar_tutor_view(request):
    return render(request, 'tutor/visualizar_tutor.html')

def anadir_tutor_view(request):
    return render(request, 'tutor/anadir_tutor.html')