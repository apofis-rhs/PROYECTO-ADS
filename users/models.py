from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- GESTOR DE USUARIOS (Logica interna de Django) ---
class UsuarioManager(BaseUserManager):
    def create_user(self, num_empleado, password=None, **extra_fields):
        if not num_empleado:
            raise ValueError('El usuario debe tener un número de empleado')
        user = self.model(num_empleado=num_empleado, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, num_empleado, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(num_empleado, password, **extra_fields)

# --- MODELOS (con base en el la BD) ---

class CatRolAdmin(models.Model):
    id_rol_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_rol_admin' # Mantener el nombre exacto de la BD, sino Django creará uno por defecto
        verbose_name = 'Rol de Administrador'
        verbose_name_plural = 'Roles de Administrador'

    def __str__(self):
        return self.nombre

class UsuarioAdmin(AbstractBaseUser, PermissionsMixin):
    # Campos del 'usuario_admin', si se agrega un campo nuevo en la BD, agregarlo aqui
    id_admin = models.AutoField(primary_key=True)
    num_empleado = models.CharField(max_length=50, unique=True)
    usuario = models.CharField(max_length=50, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    
    # Relaciones (FK)
    rol = models.ForeignKey(CatRolAdmin, on_delete=models.SET_NULL, null=True, db_column='id_rol_admin')

    # Campos requeridos por Django para el Login
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True) # Permite entrar al panel admin

    objects = UsuarioManager()

    USERNAME_FIELD = 'num_empleado'  # Campo usado para autenticar al usuario
    REQUIRED_FIELDS = ['nombre', 'correo']

    class Meta:
        db_table = 'usuario_admin'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
    
    def __str__(self):
        return f"{self.num_empleado} - {self.nombre}"