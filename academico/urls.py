from django.urls import path
from . import views

app_name = "academico"

urlpatterns = [
    # --------- Gestión de horarios (ADMIN) ----------
    path("gestion/horarios/", views.gestion_horarios_view, name="gestion_horarios"),
    path("gestion/horarios/eliminar/", views.eliminar_horarios_view, name="eliminar_horarios"),
    path("horarios/generar/form/", views.generar_horarios_form_view, name="generar_horarios_form"),

    # --------- Consultas de horarios ----------
    path("horarios/", views.lista_horarios_view, name="lista_horarios"),
    path("horarios/grupo/", views.horario_por_grupo_view, name="horario_por_grupo"),
    path("horarios/salon/", views.horario_por_salon_view, name="horario_por_salon"),

    # --------- CRUD Materias ----------
    path("materias/", views.materia_list_view, name="materia_list"),
    path("materias/nueva/", views.materia_create_view, name="materia_create"),
    path("materias/<int:pk>/editar/", views.materia_update_view, name="materia_update"),
    path("materias/<int:pk>/eliminar/", views.materia_delete_view, name="materia_delete"),

    # --------- CRUD Grupos ----------
    path("grupos/", views.grupo_list_view, name="grupo_list"),
    path("grupos/nuevo/", views.grupo_create_view, name="grupo_create"),
    path("grupos/<int:pk>/editar/", views.grupo_update_view, name="grupo_update"),
    path("grupos/<int:pk>/eliminar/", views.grupo_delete_view, name="grupo_delete"),
]
