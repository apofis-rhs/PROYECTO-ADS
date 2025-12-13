"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from academico import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ruta raiz (localhost:8000/)
    path('', views.dashboard_view, name='dashboard'),
    path('alumnos/consultar/', views.consultar_alumno_view, name='consultar_alumno'),
    path('alumnos/visualizar/<int:id_alumno>/', views.visualizar_alumno_view, name='visualizar_alumno'),
    path('alumnos/anadir/', views.anadir_alumno_view, name='anadir_alumno'),
    path('alumnos/baja/<int:id_alumno>/', views.baja_alumno_view, name='baja_alumno'),
    path('alumno/cambio-carrera/<int:id_alumno>/', views.cambio_carrera_view, name='cambio_carrera'),
    path('docentes/consultar/', views.consultar_docente_view, name='consultar_docente'),
    path('docentes/visualizar/', views.visualizar_docente_view, name='visualizar_docente'),
    path('docentes/asignar/', views.asignar_materia_view, name='asignar_materia'),
    path('docentes/anadir/', views.anadir_docente_view, name='anadir_docente'),
    path('tutores/consultar/', views.consultar_tutor_view, name='consultar_tutor'),
    path('tutores/visualizar/', views.visualizar_tutor_view, name='visualizar_tutor'),
    path('tutores/anadir/', views.anadir_tutor_view, name='anadir_tutor'),
]