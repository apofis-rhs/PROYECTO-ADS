from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Alumno, PadreTutor, Carrera, NivelEducativo, Docente, Grupo, AreaInteres,Materia,Horario
from .services import HorarioGenerator
from .forms import MateriaForm, GrupoForm
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import Grupo, Horario

def dashboard_view(request):
    return render(request, 'dashboard.html')

# -----------------------------------------------------------------------------
# VISTA PARA CONSULTAR ALUMNO
# -----------------------------------------------------------------------------

def consultar_alumno_view(request):
    query = request.GET.get('busqueda')
    if query:
        lista_alumnos = Alumno.objects.filter(boleta__icontains=query).order_by('id_alumno')
    else:
        lista_alumnos = Alumno.objects.none()
    
    return render(request, 'alumno/consultar_alumno.html', {'alumnos': lista_alumnos})

# -----------------------------------------------------------------------------
# VISTA PARA VISUALIZAR ALUMNO
# -----------------------------------------------------------------------------

def visualizar_alumno_view(request, id_alumno):
    # 1. Buscamos al alumno por ID. Si no existe, lanzamos 404.
    alumno = get_object_or_404(Alumno, pk=id_alumno)
    
    # Traemos los catálogos por si queremos editar (cambiar de nivel o tutor)
    niveles = NivelEducativo.objects.all()
    tutores = PadreTutor.objects.all()

    if request.method == 'POST':
        # AQUÍ IRÁ LA LOGICA DE (UPDATE)
        pass

    # 2. Renderizamos la plantilla con el objeto 'alumno' encontrado
    return render(request, 'alumno/visualizar_alumno.html', {
        'alumno': alumno,
        'niveles': niveles,
        'tutores': tutores
    })

#------------------------------------------------------------------------------
# VISTA PARA ALTA DE ALUMNO
#------------------------------------------------------------------------------

def anadir_alumno_view(request):
    # Obtenemos los catálogos para llenar los <select>
    niveles = NivelEducativo.objects.all()
    tutores = PadreTutor.objects.all()

    if request.method == 'POST':
        try:
            # 1. RECUPERAR DATOS OBLIGATORIOS Y CLAVE
            nombre = request.POST.get('nombre')
            ape_paterno = request.POST.get('ape_paterno')
            boleta = request.POST.get('boleta')
            id_nivel = request.POST.get('nivel')
            
            # El tutor puede venir vacío si es universidad
            id_tutor = request.POST.get('tutor')

            # 2. RECUPERAR DATOS OPCIONALES
            ape_materno = request.POST.get('ape_materno')
            curp = request.POST.get('curp')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            sexo = request.POST.get('sexo')
            nacionalidad = request.POST.get('nacionalidad')
            lugar_nacimiento = request.POST.get('lugar_nacimiento')
            direccion = request.POST.get('direccion')
            grado = request.POST.get('grado')
            
            # Recuperar la foto (si se subió alguna)
            foto = request.FILES.get('foto')

            # 3. RECUPERAR CONTACTO DE EMERGENCIA
            contacto_nombre = request.POST.get('contacto_nombre')
            contacto_parentesco = request.POST.get('contacto_parentesco')
            contacto_telefono = request.POST.get('contacto_telefono')
            contacto_telefono2 = request.POST.get('contacto_telefono2')

            # 4. VALIDACIONES DE LÓGICA DE NEGOCIO
            if not id_nivel or not boleta:
                raise ValueError("La Boleta y el Nivel Educativo son obligatorios.")

            # Validar si el tutor es obligatorio (Nivel 1, 2 o 3)
            # Convertimos a int porque desde el HTML llega como string "1"
            es_nivel_basico = int(id_nivel) <= 3
            
            if es_nivel_basico and not id_tutor:
                raise ValueError("Para Kínder, Primaria y Secundaria, asignar un Tutor es obligatorio.")

            # 5. PREPARAR OBJETOS RELACIONADOS
            nivel_obj = NivelEducativo.objects.get(id_nivel=id_nivel)
            
            tutor_obj = None
            if id_tutor:
                tutor_obj = PadreTutor.objects.get(id_tutor=id_tutor)

            # 6. CREAR EL ALUMNO
            Alumno.objects.create(
                boleta=boleta,
                nombre=nombre,
                ape_paterno=ape_paterno,
                ape_materno=ape_materno,
                curp=curp,
                fecha_nacimiento=fecha_nacimiento if fecha_nacimiento else None,
                sexo=sexo,
                nacionalidad=nacionalidad,
                lugar_nacimiento=lugar_nacimiento,
                direccion=direccion,
                grado=grado,
                foto=foto, # Guardamos la imagen
                
                # Datos de emergencia
                contacto_emergencia_nombre=contacto_nombre,
                contacto_emergencia_parentesco=contacto_parentesco,
                contacto_emergencia_telefono=contacto_telefono,
                contacto_emergencia_telefono2=contacto_telefono2,

                # Relaciones (Foreign Keys)
                nivel=nivel_obj,
                tutor=tutor_obj
            )

            # Si todo salió bien, redirigir a la consulta
            return redirect('consultar_alumno')

        except Exception as e:
            # Si algo falla (ej. boleta duplicada, o validación manual), volvemos al formulario
            # y mostramos el error.
            print(f"Error al guardar alumno: {e}")
            return render(request, 'alumno/anadir_alumno.html', {
                'niveles': niveles, 
                'tutores': tutores,
                'error': f"No se pudo guardar: {e}" # Puedes mostrar {{ error }} en tu HTML si quieres
            })

    # SI ES GET (Carga inicial de la página)
    return render(request, 'alumno/anadir_alumno.html', {
        'niveles': niveles, 
        'tutores': tutores
    })

#------------------------------------------------------------------------------
# VISTA PARA BAJA DE ALUMNO
#------------------------------------------------------------------------------

def baja_alumno_view(request, id_alumno):
    # Buscamos al alumno
    alumno = get_object_or_404(Alumno, pk=id_alumno)

    if request.method == 'POST':
        # Leemos qué opción seleccionó el usuario en el radio button
        tipo_baja = request.POST.get('tipoBaja')

        if tipo_baja == 'definitiva':
            # OPCIÓN A: Borrar permanentemente (DELETE)
            alumno.delete()
            # Redirigimos a la lista porque el alumno ya no existe
            return redirect('consultar_alumno')

        elif tipo_baja == 'temporal':
            # OPCIÓN B: Solo desactivar (UPDATE)
            alumno.activo = False
            alumno.save()
            # Redirigimos a la lista (o podrías dejarlo en visualizar)
            return redirect('consultar_alumno')

    return render(request, 'alumno/baja_alumno.html', {'alumno': alumno})

# ------------------------------------------------------------------------------
# VISTA PARA CAMBIO DE CARRERA
# ------------------------------------------------------------------------------

def cambio_carrera_view(request, id_alumno):
    # 1. Obtenemos el alumno
    alumno = get_object_or_404(Alumno, pk=id_alumno)
    
    # 2. Obtenemos las carreras disponibles (todas MENOS la actual)
    if alumno.carrera:
        carreras_disponibles = Carrera.objects.filter(activo=True).exclude(id_carrera=alumno.carrera.id_carrera)
    else:
        carreras_disponibles = Carrera.objects.filter(activo=True)

    # 3. Procesamos el cambio directo (POST)
    if request.method == 'POST':
        id_nueva_carrera = request.POST.get('nueva_carrera')
        
        if id_nueva_carrera:
            try:
                # Buscamos la carrera seleccionada
                nueva_carrera_obj = Carrera.objects.get(pk=id_nueva_carrera)
                
                # --- ACTUALIZACIÓN DIRECTA (SIMPLE) ---
                alumno.carrera = nueva_carrera_obj
                alumno.save() # Guardamos el cambio en la tabla Alumno

                messages.success(request, f'Cambio realizado. El alumno ahora está en {nueva_carrera_obj.nombre}.')
                
                # Regresamos a visualizar el perfil actualizado
                return redirect('visualizar_alumno', id_alumno=alumno.id_alumno)

            except Exception as e:
                messages.error(request, f"No se pudo realizar el cambio: {e}")
        else:
            messages.warning(request, 'Debes seleccionar una carrera.')

    # 4. Renderizamos el formulario (GET)
    return render(request, 'alumno/cambio_carrera.html', {
        'alumno': alumno,
        'carreras_disponibles': carreras_disponibles
    })

# ------------------------------------------------------------------------------
# VISTA PARA DOCENTE
# ------------------------------------------------------------------------------

def consultar_docente_view(request):
    query = request.GET.get('busqueda')
    
    if query:
        docentes = Docente.objects.filter(num_empleado__icontains=query).order_by('id_docente')
    else:
        docentes = Docente.objects.none() 

    return render(request, 'docente/consultar_docente.html', {'docentes': docentes})

# ------------------------------------------------------------------------------
# VISTA PARA VISUALIZAR DOCENTE
# ------------------------------------------------------------------------------

def visualizar_docente_view(request, id_docente):
    docente = get_object_or_404(Docente, pk=id_docente)
    
    return render(request, 'docente/visualizar_docente.html', {
        'docente': docente
    })

# ------------------------------------------------------------------------------
# VISTA PARA ASIGNAR MATERIA A DOCENTE
# ------------------------------------------------------------------------------

def asignar_materia_view(request, id_docente):
    docente = get_object_or_404(Docente, pk=id_docente)

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo_id')
        accion = request.POST.get('accion')

        if grupo_id:
            grupo = get_object_or_404(Grupo, pk=grupo_id)
            
            if accion == 'asignar':
                # VALIDACIÓN EXTRA DE SEGURIDAD:
                # Verificar que siga vacante antes de asignar (por si otro admin ganó el click)
                if grupo.docente is None:
                    grupo.docente = docente
                    grupo.save()
                    messages.success(request, f'Materia {grupo.materia.nombre} asignada correctamente.')
                else:
                    messages.error(request, f'Error: El grupo {grupo.clave_grupo} ya tiene un docente asignado.')
            
            elif accion == 'desasignar':
                grupo.docente = None
                grupo.save()
                messages.warning(request, f'Materia {grupo.materia.nombre} desasignada. Ahora está vacante.')

            return redirect('asignar_materia', id_docente=id_docente)

    # --- FILTROS ---
    
    # 1. Asignadas: Las que tiene ESTE docente
    materias_asignadas = Grupo.objects.filter(docente=docente).order_by('id_grupo')
    
    # 2. Disponibles: SOLO LAS VACANTES (Donde docente es NULL)
    #    Usamos __isnull=True para buscar campos vacíos
    materias_disponibles = Grupo.objects.filter(docente__isnull=True).order_by('id_grupo')

    return render(request, 'docente/asignar_materia.html', {
        'docente': docente,
        'materias_asignadas': materias_asignadas,
        'materias_disponibles': materias_disponibles
    })
    
# ------------------------------------------------------------------------------
# VISTA PARA ALTA DE DOCENTE
# ------------------------------------------------------------------------------

def anadir_docente_view(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 1. Recuperar datos básicos
                num_empleado = request.POST.get('num_empleado')
                nombre = request.POST.get('nombre')
                ape_paterno = request.POST.get('ape_paterno')
                ape_materno = request.POST.get('ape_materno')
                curp = request.POST.get('curp')
                rfc = request.POST.get('rfc')
                fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
                sexo = request.POST.get('sexo')
                
                # Mapeo de sexo (HTML -> BD)
                sexo_bd = 'M' if sexo == 'Masculino' else 'F' if sexo == 'Femenino' else 'O'
                
                nacionalidad = request.POST.get('nacionalidad')
                foto = request.FILES.get('foto')

                # 2. Datos de contacto y emergencia
                direccion = request.POST.get('direccion')
                contacto_nombre = request.POST.get('contacto_nombre')
                contacto_parentesco = request.POST.get('contacto_parentesco')
                contacto_telefono = request.POST.get('contacto_telefono')

                # 3. Datos Profesionales
                grado_academico = request.POST.get('grado_academico')
                institucion = request.POST.get('institucion_procedencia')
                anios_exp = request.POST.get('anios_experiencia') or 0
                especialidad_texto = request.POST.get('areas_especialidad')
                experiencia_laboral = request.POST.get('experiencia_laboral')
                certificaciones = request.POST.get('certificaciones')

                # 4. Crear el Docente
                nuevo_docente = Docente.objects.create(
                    num_empleado=num_empleado,
                    nombre=nombre,
                    ape_paterno=ape_paterno,
                    ape_materno=ape_materno,
                    curp=curp,
                    rfc=rfc,
                    fecha_nacimiento=fecha_nacimiento,
                    sexo=sexo_bd,
                    nacionalidad=nacionalidad,
                    foto=foto,
                    direccion=direccion,
                    
                    contacto_emergencia_nombre=contacto_nombre,
                    contacto_emergencia_parentesco=contacto_parentesco,
                    contacto_emergencia_telefono=contacto_telefono,
                    
                    grado_academico=grado_academico,
                    institucion_procedencia=institucion,
                    anios_experiencia=anios_exp,
                    especialidad=especialidad_texto,
                    experiencia_laboral=experiencia_laboral,
                    certificaciones=certificaciones,
                    
                    fecha_ingreso=timezone.now().date(),
                    activo=True
                )

                # 5. Manejo de Áreas de Interés
                if especialidad_texto:
                    areas_lista = [x.strip() for x in especialidad_texto.split(',')]
                    for nombre_area in areas_lista:
                        area_obj, created = AreaInteres.objects.get_or_create(nombre=nombre_area)
                        nuevo_docente.areas_interes.add(area_obj)

                messages.success(request, f'Docente {nombre} {ape_paterno} registrado exitosamente.')
                return redirect('consultar_docente')

        except Exception as e:
            messages.error(request, f'Error al guardar: {str(e)}')
            return render(request, 'docente/anadir_docente.html')

    # GET: Mostrar formulario vacío
    return render(request, 'docente/anadir_docente.html')

# ------------------------------------------------------------------------------
# VISTA CONSULTAR TUTOR
# ------------------------------------------------------------------------------

def consultar_tutor_view(request):
    query = request.GET.get('busqueda')
    
    if query:
        # Buscar tutores relacionados con alumnos cuya boleta coincida con la consulta
        tutores = PadreTutor.objects.filter(alumno__boleta__icontains=query).distinct().order_by('id_tutor')
    else:
        tutores = PadreTutor.objects.none()

    return render(request, 'tutor/consultar_tutor.html', {'tutores': tutores})

# ------------------------------------------------------------------------------
# VISTA VISUALIZAR TUTOR
# ------------------------------------------------------------------------------

def visualizar_tutor_view(request, id_tutor):
    tutor = get_object_or_404(PadreTutor, pk=id_tutor)
    hijos = tutor.alumno_set.all()

    hijo_seleccionado = None
    id_hijo_param = request.GET.get('id_hijo')

    if id_hijo_param:
        # Si el usuario selecciono uno especifico en el dropdown
        hijo_seleccionado = hijos.filter(pk=id_hijo_param).first()
    elif hijos.exists():
        # Por defecto mostramos el primero de la lista
        hijo_seleccionado = hijos.first()

    return render(request, 'tutor/visualizar_tutor.html', {
        'tutor': tutor,
        'hijos': hijos,
        'hijo_seleccionado': hijo_seleccionado
    })

# ------------------------------------------------------------------------------
# VISTA PARA ALTA DE TUTOR
# ------------------------------------------------------------------------------

def api_crear_tutor(request):
    if request.method == 'POST':
        try:
            # Crear el tutor con los datos del modal
            nuevo_tutor = PadreTutor.objects.create(
                nombre=request.POST.get('nombre'),
                ape_paterno=request.POST.get('ape_paterno'),
                ape_materno=request.POST.get('ape_materno'),
                curp=request.POST.get('curp'),
                # Ajusta 'parentesco' y 'telefono' a los nombres reales de tus campos en models.py
                # Si tu modelo usa 'telefono_principal', cámbialo aquí.
                telefono=request.POST.get('telefono'), 
                # Si tienes email en el modelo:
                # email=request.POST.get('email')
            )
            
            return JsonResponse({
                'success': True,
                'tutor_id': nuevo_tutor.id_tutor,
                'tutor_nombre': f"{nuevo_tutor.nombre} {nuevo_tutor.ape_paterno}"
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})


# ------------------------------------------------------------------------------
# CAMBIO ORDN 1
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------
# CRUD de MATERIA
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# CRUD de MATERIA
# -------------------------------------------------------------------------


def materia_list_view(request):
    """
    Lista de materias con filtros por nivel educativo y grado (nivel_sugerido).
    """
    # Leer filtros desde la query string (?id_nivel=...&grado=...)
    nivel_id_raw = (request.GET.get("id_nivel") or "").strip()
    grado_raw = (request.GET.get("grado") or "").strip()

    materias_qs = (
        Materia.objects
        .select_related("nivel_educativo", "carrera")
        .order_by("nivel_educativo__nombre", "nivel_sugerido", "clave")
    )

    # Filtro por nivel educativo
    if nivel_id_raw:
        try:
            nivel_id_int = int(nivel_id_raw)
            materias_qs = materias_qs.filter(nivel_educativo_id=nivel_id_int)
        except ValueError:
            nivel_id_int = None
    else:
        nivel_id_int = None

    # Filtro por grado / nivel sugerido
    if grado_raw:
        try:
            grado_int = int(grado_raw)
            materias_qs = materias_qs.filter(nivel_sugerido=grado_int)
        except ValueError:
            grado_int = None
    else:
        grado_int = None

    niveles = NivelEducativo.objects.all().order_by("nombre")

    context = {
        "materias": materias_qs,
        "niveles": niveles,
        "filtros": {
            "id_nivel": nivel_id_int,
            "grado": grado_raw,  # lo dejamos como texto para rellenar el input
        },
    }
    return render(request, "gestion/materia_list.html", context)



def materia_create_view(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Materia creada correctamente.")
            return redirect("academico:materia_list")
    else:
        form = MateriaForm()

    return render(request, "gestion/materia_form.html", {"form": form})


def materia_update_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    if request.method == "POST":
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            messages.success(request, "Materia actualizada correctamente.")
            return redirect("academico:materia_list")
    else:
        form = MateriaForm(instance=materia)

    return render(
        request,
        "gestion/materia_form.html",
        {"form": form, "materia": materia},
    )


def materia_delete_view(request, pk):
    materia = get_object_or_404(Materia, pk=pk)

    if request.method == "POST":
        materia.delete()
        messages.success(request, "Materia eliminada correctamente.")
        return redirect("academico:materia_list")

    return render(request, "gestion/materia_confirm_delete.html", {"materia": materia})

# -------------------------------------------------------------------------
# CRUD de GRUPO
# -------------------------------------------------------------------------


def grupo_list_view(request):
    """
    Lista de grupos (salon + materia + docente).
    """
    grupos = (
        Grupo.objects
        .select_related("nivel", "turno", "materia", "docente")
        .order_by("nivel__nombre", "grado", "clave_grupo", "materia__nombre")
    )
    return render(request, "gestion/grupo_list.html", {"grupos": grupos})


def grupo_create_view(request):
    """
    Crear un nuevo grupo (salon + materia).
    La generacion de horarios se hace en el modulo 'Generar horarios'.
    """
    initial = {}
    periodo = request.GET.get("periodo")
    id_nivel = request.GET.get("id_nivel")

    if periodo:
        initial["periodo"] = periodo
    if id_nivel:
        initial["nivel"] = id_nivel  # ModelForm convierte PK -> objeto

    if request.method == "POST":
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo creado correctamente.")
            return redirect("academico:grupo_list")
    else:
        form = GrupoForm(initial=initial)

    return render(request, "gestion/grupo_form.html", {"form": form})


def grupo_update_view(request, pk):
    """
    Editar un grupo existente.
    """
    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method == "POST":
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo actualizado correctamente.")
            return redirect("academico:grupo_list")
    else:
        form = GrupoForm(instance=grupo)

    return render(request, "gestion/grupo_form.html", {"form": form, "grupo": grupo})


def grupo_delete_view(request, pk):
    """
    Eliminar un grupo. Por el on_delete=CASCADE en Horario,
    tambien se borran sus horarios asociados.
    """
    grupo = get_object_or_404(Grupo, pk=pk)

    if request.method == "POST":
        grupo.delete()
        messages.success(request, "Grupo eliminado correctamente.")
        return redirect("academico:grupo_list")

    return render(request, "gestion/grupo_confirm_delete.html", {"grupo": grupo})

# -------------------------------------------------------------------------
# VISTAS PARA GESTION DE HORARIOS
# -------------------------------------------------------------------------


def gestion_horarios_view(request):
    """
    Pantalla principal de gestion de horarios.
    Desde aqui el usuario puede:
      - Generar horarios
      - Visualizar horarios
      - Eliminar horarios
    """
    return render(request, "gestion/horarios_dashboard.html")


def eliminar_horarios_view(request):
    """
    Vista para eliminar horarios.

    Permite:
      - Eliminar TODOS los horarios del sistema.
      - Eliminar solo los horarios de uno o varios salones
        (combinacion clave_grupo + periodo).
    """
    total = Horario.objects.count()

    salones_qs = (
        Grupo.objects
        .values("clave_grupo", "periodo", "grado", "nivel__nombre")
        .distinct()
        .order_by("nivel__nombre", "grado", "clave_grupo", "periodo")
    )

    salones = []
    for s in salones_qs:
        grupos_salon = Grupo.objects.filter(
            clave_grupo=s["clave_grupo"],
            periodo=s["periodo"],
        )
        total_salon = Horario.objects.filter(grupo__in=grupos_salon).count()
        if total_salon == 0:
            continue

        value = f'{s["clave_grupo"]}|{s["periodo"]}'
        label = f'{s["nivel__nombre"]} - {s["grado"]} - {s["clave_grupo"]} ({s["periodo"]})'

        salones.append(
            {
                "value": value,
                "label": label,
                "total_salon": total_salon,
            }
        )

    if request.method == "POST":
        accion = request.POST.get("accion")

        # Eliminar horarios de salones seleccionados
        if accion == "eliminar_seleccionados":
            seleccionados = request.POST.getlist("salones")

            if not seleccionados:
                messages.warning(
                    request,
                    "Debes seleccionar al menos un salon para eliminar sus horarios.",
                )
            else:
                total_eliminados = 0

                for salon_value in seleccionados:
                    try:
                        clave_grupo, periodo = salon_value.split("|", 1)
                    except ValueError:
                        continue

                    grupos_salon = Grupo.objects.filter(
                        clave_grupo=clave_grupo,
                        periodo=periodo,
                    )
                    qs = Horario.objects.filter(grupo__in=grupos_salon)
                    count = qs.count()
                    if count:
                        total_eliminados += count
                        qs.delete()

                messages.success(
                    request,
                    f"Se eliminaron {total_eliminados} horarios de los salones seleccionados.",
                )
                return redirect("academico:gestion_horarios")

        # Eliminar TODOS los horarios
        elif accion == "eliminar_todos":
            total_eliminados = Horario.objects.count()
            Horario.objects.all().delete()
            messages.success(
                request,
                f"Se eliminaron {total_eliminados} horarios de todos los salones.",
            )
            return redirect("academico:gestion_horarios")

        # Cancelar
        else:
            return redirect("academico:gestion_horarios")

    context = {
        "total": total,
        "salones": salones,
    }
    return render(request, "gestion/horarios_eliminar.html", context)


def lista_horarios_view(request):
    """
    Muestra los horarios generados en una tabla simple.
    Se pueden filtrar por nivel, periodo y grado.
    """
    nivel_id = request.GET.get("id_nivel")
    periodo = request.GET.get("periodo")
    grado = request.GET.get("grado")

    horarios_qs = (
        Horario.objects
        .select_related("grupo", "grupo__materia", "grupo__docente", "grupo__nivel")
        .order_by(
            "grupo__nivel__nombre",
            "grupo__grado",
            "grupo__clave_grupo",
            "dia_semana",
            "hora_inicio",
        )
    )

    if nivel_id:
        horarios_qs = horarios_qs.filter(grupo__nivel_id=nivel_id)
    if periodo:
        horarios_qs = horarios_qs.filter(grupo__periodo=periodo)
    if grado:
        horarios_qs = horarios_qs.filter(grupo__grado=grado)

    DIAS = {
        1: "Lunes",
        2: "Martes",
        3: "Miercoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sabado",
        7: "Domingo",
    }

    horarios = []
    for h in horarios_qs:
        docente = h.grupo.docente
        horarios.append(
            {
                "id_grupo": h.grupo.id_grupo,
                "grupo": h.grupo.clave_grupo,
                "nivel": h.grupo.nivel.nombre if h.grupo.nivel else "",
                "grado": h.grupo.grado,
                "periodo": h.grupo.periodo,
                "materia": h.grupo.materia.nombre,
                "docente": (
                    f"{docente.nombre} {docente.ape_paterno}" if docente else ""
                ),
                "dia": DIAS.get(h.dia_semana, h.dia_semana),
                "hora_inicio": h.hora_inicio,
                "hora_fin": h.hora_fin,
                "aula": h.aula or "",
            }
        )

    context = {
        "horarios": horarios,
        "niveles": NivelEducativo.objects.all().order_by("id_nivel"),
        "filtros": {
            "id_nivel": nivel_id or "",
            "periodo": periodo or "",
            "grado": grado or "",
        },
    }
    return render(request, "gestion/horarios_lista.html", context)


def generar_horarios_form_view(request):
    """
    Formulario para elegir periodo, nivel y grado/semestre.
    Permite:
      - Previsualizar los grupos encontrados.
      - Generar horarios usando HorarioGenerator solo para los grupos seleccionados
        (o para todos los filtrados si no se marca ninguno).
    """
    niveles = NivelEducativo.objects.all().order_by("id_nivel")

    mensaje = None
    errores: list[str] = []
    grupos_filtrados = []
    valores = {
        "periodo": "",
        "id_nivel": None,
        "grado": "",
        "semestre": "",
        "tipo_alumno": "",
        "id_carrera": "",
    }

    if request.method == "POST":
        accion = request.POST.get("accion") or "generar"

        periodo = (request.POST.get("periodo") or "").strip()
        id_nivel = (request.POST.get("id_nivel") or "").strip()
        grado = (request.POST.get("grado") or "").strip()
        semestre = (request.POST.get("semestre") or "").strip()
        tipo_alumno = (request.POST.get("tipo_alumno") or "").strip()
        id_carrera = (request.POST.get("id_carrera") or "").strip()

        # Guardamos los valores para rellenar el formulario
        try:
            id_nivel_int = int(id_nivel) if id_nivel else None
        except ValueError:
            id_nivel_int = None

        valores = {
            "periodo": periodo,
            "id_nivel": id_nivel_int,
            "grado": grado,
            "semestre": semestre,
            "tipo_alumno": tipo_alumno,
            "id_carrera": id_carrera,
        }

        # Validacion basica
        if not periodo or not id_nivel:
            errores.append("Debes indicar al menos el Periodo y el Nivel educativo.")

        if not errores:
            generator = HorarioGenerator(
                periodo=periodo,
                id_nivel=id_nivel,
                grado=grado,
                semestre=semestre,
                tipo_alumno=tipo_alumno,
                id_carrera=id_carrera,
            )

            # 1) PREVISUALIZAR GRUPOS
            if accion == "previsualizar":
                nivel = generator._obtener_nivel()
                if not nivel:
                    errores.append("No se encontro el nivel educativo seleccionado.")
                else:
                    grupos_filtrados = generator._obtener_grupos(nivel)
                    if not grupos_filtrados:
                        mensaje = "No se encontraron grupos con esos filtros."

            # 2) GENERAR HORARIOS
            elif accion == "generar":
                grupo_ids_raw = request.POST.getlist("grupo_ids")
                grupos_ids = []
                for v in grupo_ids_raw:
                    try:
                        grupos_ids.append(int(v))
                    except ValueError:
                        continue

                if grupos_ids:
                    generator.grupos_ids_seleccionados = grupos_ids

                resultado = generator.generar()

                if resultado.es_valido:
                    mensaje = (
                        "Horarios generados correctamente. "
                        f"Asignaciones: {resultado.total_asignaciones}"
                    )
                else:
                    errores = resultado.errores

    context = {
        "niveles": niveles,
        "mensaje": mensaje,
        "errores": errores,
        "grupos_filtrados": grupos_filtrados,
        "valores": valores,
    }
    return render(request, "gestion/horarios_generar_form.html", context)


def horario_por_grupo_view(request):
    """
    Permite seleccionar un grupo y muestra su horario en formato de cuadricula:

        columnas = dias (Lunes a Viernes)
        filas    = rangos horarios (07:00-08:30, 08:30-10:00, ...)

    Cada celda contiene el nombre de la materia (o queda vacia si no hay clase).
    """
    grupos = (
        Grupo.objects
        .select_related("nivel", "materia", "docente")
        .order_by("nivel__nombre", "grado", "clave_grupo")
    )

    grupo_id = request.GET.get("grupo_id")
    grupo_seleccionado = None
    filas = []
    dias = [
        {"id": 1, "nombre": "Lunes"},
        {"id": 2, "nombre": "Martes"},
        {"id": 3, "nombre": "Miercoles"},
        {"id": 4, "nombre": "Jueves"},
        {"id": 5, "nombre": "Viernes"},
    ]

    if grupo_id:
        grupo_seleccionado = get_object_or_404(Grupo, pk=grupo_id)

        horarios = (
            Horario.objects.filter(grupo=grupo_seleccionado)
            .order_by("dia_semana", "hora_inicio")
        )

        if horarios.exists():
            rangos = sorted(
                {(h.hora_inicio, h.hora_fin) for h in horarios},
                key=lambda x: (x[0], x[1]),
            )

            celdas = defaultdict(dict)
            for h in horarios:
                clave_rango = (h.hora_inicio, h.hora_fin)
                nombre_materia = h.grupo.materia.nombre
                celdas[h.dia_semana][clave_rango] = nombre_materia

            for inicio, fin in rangos:
                rango_str = f"{inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}"
                fila = {"rango": rango_str, "celdas": []}
                for d in dias:
                    texto = celdas[d["id"]].get((inicio, fin), "")
                    fila["celdas"].append(texto)
                filas.append(fila)

    context = {
        "grupos": grupos,
        "grupo_seleccionado": grupo_seleccionado,
        "dias": dias,
        "filas": filas,
    }
    return render(request, "gestion/horario_por_grupo.html", context)


def horario_por_salon_view(request):
    """
    Muestra el horario semanal para un salon (clave_grupo + periodo),
    armando una cuadricula de Horas x Dias con la materia y el docente.
    """
    salones_qs = (
        Grupo.objects
        .values("clave_grupo", "periodo", "grado", "nivel__nombre")
        .distinct()
        .order_by("nivel__nombre", "grado", "clave_grupo", "periodo")
    )

    salones = []
    for s in salones_qs:
        value = f'{s["clave_grupo"]}|{s["periodo"]}'
        label = f'{s["nivel__nombre"]} - {s["grado"]} - {s["clave_grupo"]} ({s["periodo"]})'
        salones.append(
            {
                "value": value,
                "clave_grupo": s["clave_grupo"],
                "periodo": s["periodo"],
                "grado": s["grado"],
                "nivel_nombre": s["nivel__nombre"],
                "label": label,
                "selected": False,
            }
        )

    salon_value = request.GET.get("salon")
    if not salon_value and salones:
        salon_value = salones[0]["value"]

    clave_grupo = None
    periodo = None
    if salon_value:
        try:
            clave_grupo, periodo = salon_value.split("|", 1)
        except ValueError:
            clave_grupo, periodo = None, None

    for s in salones:
        s["selected"] = (s["value"] == salon_value)

    dias = [
        {"id": 1, "nombre": "Lun"},
        {"id": 2, "nombre": "Mar"},
        {"id": 3, "nombre": "Mie"},
        {"id": 4, "nombre": "Jue"},
        {"id": 5, "nombre": "Vie"},
    ]

    filas = []

    if clave_grupo and periodo:
        grupos_salon = Grupo.objects.filter(
            clave_grupo=clave_grupo,
            periodo=periodo,
        )

        horarios_qs = (
            Horario.objects
            .filter(grupo__in=grupos_salon)
            .select_related("grupo", "grupo__materia", "grupo__docente")
            .order_by("dia_semana", "hora_inicio")
        )

        if horarios_qs.exists():
            rangos = sorted(
                {(h.hora_inicio, h.hora_fin) for h in horarios_qs},
                key=lambda x: (x[0], x[1]),
            )

            celdas = defaultdict(list)
            for h in horarios_qs:
                key = (h.dia_semana, h.hora_inicio, h.hora_fin)
                materia = h.grupo.materia
                docente = h.grupo.docente
                texto = materia.nombre
                if docente:
                    texto += f"\n{docente.nombre} {docente.ape_paterno}"
                celdas[key].append(texto)

            for inicio, fin in rangos:
                rango_str = f"{inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}"
                fila = {"rango": rango_str, "celdas": []}

                for d in dias:
                    key = (d["id"], inicio, fin)
                    asign = celdas.get(key, [])

                    if not asign:
                        celda_texto = ""
                    elif len(asign) == 1:
                        celda_texto = asign[0]
                    else:
                        celda_texto = "CONFLICTO\n" + " / ".join(asign)

                    fila["celdas"].append(celda_texto)

                filas.append(fila)

    context = {
        "salones": salones,
        "dias": dias,
        "filas": filas,
        "salon_value": salon_value or "",
        "clave_grupo": clave_grupo or "",
        "periodo": periodo or "",
    }
    return render(request, "gestion/horario_por_salon.html", context)
