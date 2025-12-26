from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Alumno, PadreTutor, Carrera, NivelEducativo, Docente, Grupo, AreaInteres, HistorialAcademico, Incidente

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
# VISTA PARA RENDERIZAR PDF
# ------------------------------------------------------------------------------

def render_pdf(template_src, context_dict={}):
    """Función auxiliar para renderizar HTML a PDF"""
    template = get_template(template_src)
    html  = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    # Descarga directa: attachment; filename="report.pdf"
    # Visualizar en navegador: inline; filename="report.pdf"
    response['Content-Disposition'] = 'inline; filename="documento.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Tuvimos errores <pre>' + html + '</pre>')
    return response

# ------------------------------------------------------------------------------
# VISTA PARA GENERAR DOCUMENTO PDF DEL ALUMNO
# ------------------------------------------------------------------------------

def generar_documento_alumno(request, id_alumno):
    tipo_documento = request.GET.get('tipo')
    alumno = get_object_or_404(Alumno, pk=id_alumno)

    context = {'alumno': alumno}
    template_name = ""

    if tipo_documento == 'horario':
        # Corrección anterior: 'alumnogrupo_set' en lugar de 'alumno_grupo_set'
        grupos = alumno.alumnogrupo_set.all() 
        context['grupos'] = grupos
        template_name = 'pdfs/documento_horario.html'

    elif tipo_documento == 'historial':
        # --- CORRECCIÓN AQUÍ ---
        # Cambiamos 'id_alumno=' por 'alumno='
        historial = HistorialAcademico.objects.filter(alumno=alumno)
        context['historial'] = historial
        template_name = 'pdfs/documento_historial.html'

    elif tipo_documento == 'incidencias':
        incidencias = Incidente.objects.filter(alumno=alumno)
        context['incidencias'] = incidencias
        template_name = 'pdfs/documento_incidencias.html'
        
    elif tipo_documento == 'ficha':
        # Solo necesitamos los datos del alumno, que ya están en el context
        template_name = 'pdfs/documento_ficha.html'

    else:
        return HttpResponse("Tipo de documento no válido.")

    return render_pdf(template_name, context)

# ------------------------------------------------------------------------------
# VISTA PARA GENERAR DOCUMENTO PDF DEL DOCENTE
# ------------------------------------------------------------------------------

def generar_documento_docente(request, id_docente):
    # 1. Obtenemos parámetros
    tipo_documento = request.GET.get('tipo')
    docente = get_object_or_404(Docente, pk=id_docente)

    context = {'docente': docente}
    template_name = ""

    # 2. Lógica segun el reporte
    if tipo_documento == 'horario':
        # Buscamos los grupos donde este docente da clases
        grupos = Grupo.objects.filter(docente=docente)
        context['grupos'] = grupos
        template_name = 'pdfs/docente_horario.html'

    elif tipo_documento == 'incidencias':
        # Buscamos incidentes donde este docente este involucrado
        incidencias = Incidente.objects.filter(docente=docente).order_by('-fecha')
        context['incidencias'] = incidencias
        template_name = 'pdfs/docente_incidencias.html'
    
    elif tipo_documento == 'ficha':
        # Placeholder para la ficha tecnica
        template_name = 'pdfs/docente_ficha.html'

    else:
        return HttpResponse("Tipo de documento no válido.")

    # 3. Generar PDF
    return render_pdf(template_name, context)