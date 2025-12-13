from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alumno, Carrera, NivelEducativo, PadreTutor

def dashboard_view(request):
    return render(request, 'dashboard.html')


def consultar_alumno_view(request):
    query = request.GET.get('busqueda')
    if query:
        lista_alumnos = Alumno.objects.filter(boleta__icontains=query).order_by('id_alumno')
    else:
        lista_alumnos = Alumno.objects.none()
    
    return render(request, 'alumno/consultar_alumno.html', {'alumnos': lista_alumnos})


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