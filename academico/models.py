from django.db import models

from django.db import models

# --- CATALOGOS ---
class NivelEducativo(models.Model):
    id_nivel = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'nivel_educativo'
        verbose_name = 'Nivel Educativo'
    def __str__(self): return self.nombre

class CatTipoRelacionTutor(models.Model):
    id_tipo_relacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_tipo_relacion_tutor'
        verbose_name = 'Tipo de Relación (Tutor)'
    def __str__(self): return self.nombre

# --- TABLAS PRINCIPALES ---

class PadreTutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    # NUEVO:
    foto = models.CharField(max_length=255, null=True, blank=True, default='/static/img/tutor_placeholder.png')
    
    tipo_relacion = models.ForeignKey('CatTipoRelacionTutor', on_delete=models.SET_NULL, null=True, db_column='id_tipo_relacion')

    class Meta:
        db_table = 'padre_tutor'
        verbose_name = 'Padre o Tutor'

    def __str__(self):
        return f"{self.nombre} {self.ape_paterno}"

class Docente(models.Model):
    id_docente = models.AutoField(primary_key=True)
    num_empleado = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    # NUEVO:
    foto = models.CharField(max_length=255, null=True, blank=True, default='/static/img/docente_placeholder.png')
    
    fecha_ingreso = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'docente'
        verbose_name = 'Docente'

    def __str__(self):
        return f"{self.num_empleado} - {self.nombre}"

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    boleta = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    ape_paterno = models.CharField(max_length=100)
    ape_materno = models.CharField(max_length=100, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    # NUEVOS CAMPOS DEL MAQUETADO:
    direccion = models.CharField(max_length=200, null=True, blank=True)
    contacto_emergencia_nombre = models.CharField(max_length=100, null=True, blank=True)
    contacto_emergencia_telefono = models.CharField(max_length=20, null=True, blank=True)
    foto = models.CharField(max_length=255, null=True, blank=True, default='/static/img/alumno_placeholder.png')

    # Relaciones
    nivel = models.ForeignKey('NivelEducativo', on_delete=models.CASCADE, db_column='id_nivel')
    tutor = models.ForeignKey(PadreTutor, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_tutor')
    
    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'

    def __str__(self):
        return f"{self.boleta} - {self.nombre}"

    # Logica para mostrar Contacto de Emergencia (Simulando el maquetado)
    def contacto_emergencia(self):
        if self.tutor:
            return f"{self.tutor.nombre} ({self.tutor.telefono})"
        return "No asignado"