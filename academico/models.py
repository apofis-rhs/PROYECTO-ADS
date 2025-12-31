from django.db import models
# IMPORTANTE: Importamos el modelo de la otra app para evitar el error de duplicidad
from users.models import UsuarioAdmin 

# Opciones generales
SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
]

# -------------------------------------------------------------------------
# 1) CATÁLOGOS Y TABLAS DE APOYO
# -------------------------------------------------------------------------

class NivelEducativo(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'nivel_educativo'
        verbose_name = 'Nivel Educativo'
        verbose_name_plural = 'Niveles Educativos'

    def __str__(self):
        return self.nombre

class Universidad(models.Model):
    id_universidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    pais = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'universidad'
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'

    def __str__(self):
        return self.nombre

class AreaInteres(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'area_interes'
        verbose_name = 'Área de Interés'
        verbose_name_plural = 'Áreas de Interés'

    def __str__(self):
        return self.nombre

class CatTipoRelacionTutor(models.Model):
    id_tipo_relacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_tipo_relacion_tutor'
        verbose_name = 'Tipo Relación Tutor'

    def __str__(self):
        return self.nombre

class CatTipoCarrera(models.Model):
    id_tipo_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    class Meta:
        db_table = 'cat_tipo_carrera'
        verbose_name = 'Tipo de Carrera'

    def __str__(self):
        return self.nombre

class CatTurno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_turno'
        verbose_name = 'Turno'

    def __str__(self):
        return self.nombre

class CatEstadoAlumno(models.Model):
    id_estado_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_estado_alumno'
        verbose_name = 'Estado del Alumno'

    def __str__(self):
        return self.nombre

class CatEstadoInscripcion(models.Model):
    id_estado_inscripcion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_estado_inscripcion'
        verbose_name = 'Estado de Inscripción'

    def __str__(self):
        return self.nombre

class CatTipoIncidente(models.Model):
    id_tipo_incidente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_tipo_incidente'
        verbose_name = 'Tipo de Incidente'

    def __str__(self):
        return self.nombre

class CatGravedadIncidente(models.Model):
    id_gravedad_incidente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_gravedad_incidente'
        verbose_name = 'Gravedad del Incidente'

    def __str__(self):
        return self.nombre

class CatEstadoHistorial(models.Model):
    id_estado_historial = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = 'cat_estado_historial'
        verbose_name = 'Estado del Historial'

    def __str__(self):
        return self.nombre

# -------------------------------------------------------------------------
# 2) PADRE / TUTOR
# -------------------------------------------------------------------------

class PadreTutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    
    curp = models.CharField(max_length=18, null=True, blank=True, unique=True)
    telefono_secundario = models.CharField(max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to='tutores/', null=True, blank=True, default='tutor_placeholder.png')

    tipo_relacion = models.ForeignKey(CatTipoRelacionTutor, on_delete=models.SET_NULL, null=True, db_column='id_tipo_relacion')

    class Meta:
        db_table = 'padre_tutor'
        verbose_name = 'Padre o Tutor'
        verbose_name_plural = 'Padres o Tutores'

    def __str__(self):
        return f"{self.nombre} {self.ape_paterno}"

# -------------------------------------------------------------------------
# 3) DOCENTE
# -------------------------------------------------------------------------

class Docente(models.Model):
    id_docente = models.AutoField(primary_key=True)
    num_empleado = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    curp = models.CharField(max_length=18, null=True, blank=True, unique=True)
    rfc = models.CharField(max_length=13, null=True, blank=True, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    nacionalidad = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    foto = models.ImageField(upload_to='docentes/', null=True, blank=True, default='docente_placeholder.png')

    contacto_emergencia_nombre = models.CharField(max_length=100, null=True, blank=True)
    contacto_emergencia_parentesco = models.CharField(max_length=50, null=True, blank=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, null=True, blank=True)

    grado_academico = models.CharField(max_length=100, null=True, blank=True)
    institucion_procedencia = models.CharField(max_length=150, null=True, blank=True)
    anios_experiencia = models.IntegerField(null=True, blank=True)
    experiencia_laboral = models.TextField(null=True, blank=True)
    certificaciones = models.TextField(null=True, blank=True)

    areas_interes = models.ManyToManyField(
        AreaInteres,
        db_table='docente_area_interes',
        blank=True
    )

    class Meta:
        db_table = 'docente'
        verbose_name = 'Docente'

    def __str__(self):
        return f"{self.num_empleado} - {self.nombre} {self.ape_paterno}"

# -------------------------------------------------------------------------
# 4) CARRERAS Y MATERIAS
# -------------------------------------------------------------------------

class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    duracion_semestres = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_universidad')
    tipo_carrera = models.ForeignKey(CatTipoCarrera, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_tipo_carrera')

    class Meta:
        db_table = 'carrera'
        verbose_name = 'Carrera'

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    creditos = models.IntegerField(default=7)
    nivel_sugerido = models.IntegerField(null=True, blank=True) 

    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True, db_column='id_carrera')
    nivel_educativo = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, db_column='id_nivel')
    sesiones_por_semana = models.IntegerField(default=5)

    class Meta:
        db_table = 'materia'
        verbose_name = 'Materia'

    def __str__(self):
        return f"{self.clave} - {self.nombre}"

# -------------------------------------------------------------------------
# 5) ALUMNO
# -------------------------------------------------------------------------

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    boleta = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    fecha_alta = models.DateField(null=True, blank=True)
    semestre_actual = models.IntegerField(null=True, blank=True)

    curp = models.CharField(max_length=18, null=True, blank=True, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    nacionalidad = models.CharField(max_length=100, null=True, blank=True)
    lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    foto = models.ImageField(upload_to='alumnos/', null=True, blank=True, default='alumno_placeholder.png')
    
    contacto_emergencia_nombre = models.CharField(max_length=100, null=True, blank=True)
    contacto_emergencia_parentesco = models.CharField(max_length=50, null=True, blank=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, null=True, blank=True)
    contacto_emergencia_telefono2 = models.CharField(max_length=20, null=True, blank=True)

    estado_alumno = models.ForeignKey(CatEstadoAlumno, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_estado_alumno')
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, db_column='id_nivel')
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_carrera')
    tutor = models.ForeignKey(PadreTutor, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_tutor')

    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'

    def __str__(self):
        return f"{self.boleta} - {self.nombre} {self.ape_paterno}"

# -------------------------------------------------------------------------
# 6) GRUPOS Y HORARIOS
# -------------------------------------------------------------------------

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    clave_grupo = models.CharField(max_length=50)
    grado = models.IntegerField(null=True, blank=True)
    periodo = models.CharField(max_length=20)
    
    turno = models.ForeignKey(CatTurno, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_turno')
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, db_column='id_nivel')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, db_column='id_materia')
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_docente')

    alumnos = models.ManyToManyField(Alumno, through='AlumnoGrupo')

    class Meta:
        db_table = 'grupo'
        verbose_name = 'Grupo'

    def __str__(self):
        return f"{self.clave_grupo} - {self.materia.nombre}"

class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    dia_semana = models.SmallIntegerField() 
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=50, null=True, blank=True)
    
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo')

    class Meta:
        db_table = 'horario'
        verbose_name = 'Horario'

# -------------------------------------------------------------------------
# 7) INSCRIPCIONES (Tabla Intermedia)
# -------------------------------------------------------------------------

class AlumnoGrupo(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, db_column='id_grupo')
    estado_inscripcion = models.ForeignKey(CatEstadoInscripcion, on_delete=models.SET_NULL, null=True, db_column='id_estado_inscripcion')
    fecha_inscripcion = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'alumno_grupo'
        unique_together = (('alumno', 'grupo'),)
        verbose_name = 'Inscripción Grupo'
        verbose_name_plural = 'Inscripciones Grupos'

# -------------------------------------------------------------------------
# 8) HISTORIAL ACADÉMICO
# -------------------------------------------------------------------------

class HistorialAcademico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    periodo = models.CharField(max_length=20)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, db_column='id_materia')
    estado_historial = models.ForeignKey(CatEstadoHistorial, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_estado_historial')

    class Meta:
        db_table = 'historial_academico'
        verbose_name = 'Historial Académico'

    def __str__(self):
        return f"{self.alumno.boleta} - {self.materia.clave}: {self.calificacion}"

# -------------------------------------------------------------------------
# 9) INCIDENTES
# -------------------------------------------------------------------------

class Incidente(models.Model):
    id_incidente = models.AutoField(primary_key=True)
    fecha = models.DateField()
    descripcion = models.TextField()
    
    tipo_incidente = models.ForeignKey(CatTipoIncidente, on_delete=models.CASCADE, db_column='id_tipo_incidente')
    gravedad = models.ForeignKey(CatGravedadIncidente, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_gravedad_incidente')
    alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_alumno')
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_docente')
    
    # Aquí es donde usamos el modelo importado de la app 'users'
    admin = models.ForeignKey(UsuarioAdmin, on_delete=models.CASCADE, db_column='id_admin')

    class Meta:
        db_table = 'incidente'
        verbose_name = 'Incidente'

    def __str__(self):
        return f"Incidente {self.id_incidente} - {self.fecha}"

# -------------------------------------------------------------------------
# 10) REGLAS DE HORARIO Y DISPONIBILIDAD
# -------------------------------------------------------------------------

class ReglaHorario(models.Model):
    id_regla = models.AutoField(primary_key=True)
    # Relación con nivel educativo (kinder, primaria, secundaria, prepa, universidad)
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, db_column='id_nivel')

    # Para universidad (opcional)
    semestre = models.IntegerField(null=True, blank=True)
    tipo_alumno = models.CharField(
        max_length=20,
        null=True,
        blank=True  # 'NUEVO_INGRESO', 'POSTERIOR' o null para K–Prepa
    )

    # Parámetros principales
    duracion_bloque_min = models.IntegerField()          # ej. 90
    materias_max_por_dia = models.IntegerField()         # ej. 5
    descanso_duracion_min = models.IntegerField()        # ej. 30
    descanso_despues_bloque = models.IntegerField()      # ej. 2

    permitir_taller = models.BooleanField(default=False)
    bloque_taller = models.IntegerField(null=True, blank=True)

    carga_docente_max = models.IntegerField()            # ej. 4
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'regla_horario'
        verbose_name = 'Regla de horario'
        verbose_name_plural = 'Reglas de horario'

    def __str__(self):
        return f"Regla {self.id_regla} - {self.nivel.nombre}"


class DisponibilidadDocente(models.Model):
    id_disponibilidad = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, db_column='id_docente')
    dia_semana = models.SmallIntegerField()  # 1=Lunes ... 7=Domingo
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = 'disponibilidad_docente'
        verbose_name = 'Disponibilidad docente'
        verbose_name_plural = 'Disponibilidades docentes'

    def __str__(self):
        return f"{self.docente.nombre} - día {self.dia_semana}"


class DocenteMateria(models.Model):
    id_docente_materia = models.AutoField(primary_key=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, db_column='id_docente')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, db_column='id_materia')
    prioridad = models.SmallIntegerField(default=1)  # 1 = titular, 2 = suplente, etc.

    class Meta:
        db_table = 'docente_materia'
        verbose_name = 'Docente por materia'
        verbose_name_plural = 'Docentes por materia'
        unique_together = ('docente', 'materia')

    def __str__(self):
        return f"{self.docente.nombre} -> {self.materia.nombre} (prio {self.prioridad})"
