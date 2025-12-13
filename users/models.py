from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# -------------------------------------------------------------------------
# 1) CATÁLOGO DE ROLES (ADMINISTRATIVO)
# -------------------------------------------------------------------------

class CatRolAdmin(models.Model):
    id_rol_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        db_table = 'cat_rol_admin'
        verbose_name = 'Rol de Administrador'
        verbose_name_plural = 'Roles de Administrador'

    def __str__(self):
        return self.nombre

# -------------------------------------------------------------------------
# 2) MANAGER DE USUARIO (Requerido por Django Auth)
# -------------------------------------------------------------------------

class UsuarioAdminManager(BaseUserManager):
    def create_user(self, usuario, num_empleado, correo, password=None, **extra_fields):
        if not usuario:
            raise ValueError('El usuario es obligatorio')
        if not num_empleado:
            raise ValueError('El número de empleado es obligatorio')
        
        email = self.normalize_email(correo)
        user = self.model(usuario=usuario, num_empleado=num_empleado, correo=email, **extra_fields)
        
        # set_password encripta la contraseña automáticamente
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, num_empleado, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Aseguramos que tenga un rol por defecto si es superusuario (opcional)
        # Podrías necesitar crear un rol dummy o manejar esto según tu lógica
        # extra_fields.setdefault('rol_id', 1) 

        return self.create_user(usuario, num_empleado, correo, password, **extra_fields)

# -------------------------------------------------------------------------
# 3) USUARIO ADMINISTRADOR (Modelo Custom Auth)
# -------------------------------------------------------------------------

class UsuarioAdmin(AbstractBaseUser, PermissionsMixin):
    id_admin = models.AutoField(primary_key=True)
    num_empleado = models.CharField(max_length=50, unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    
    # AbstractBaseUser ya trae un campo 'password', pero para mapearlo a tu columna
    # 'password_hash' de la BD, lo redefinimos apuntando a esa columna.
    password = models.CharField(max_length=255, db_column='password_hash')
    
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    
    # Relación con Rol (permitimos null temporalmente para evitar errores al crear superuser por consola)
    rol = models.ForeignKey(CatRolAdmin, on_delete=models.CASCADE, db_column='id_rol_admin', null=True, blank=True)

    # Campos requeridos por Django para el manejo de sesiones y admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Necesario para entrar al admin de Django

    objects = UsuarioAdminManager()

    # CONFIGURACIÓN DE AUTH
    USERNAME_FIELD = 'usuario'  # Campo con el que harás login
    REQUIRED_FIELDS = ['num_empleado', 'correo', 'nombre'] # Campos que te pedirá al crear superuser

    class Meta:
        db_table = 'usuario_admin'
        verbose_name = 'Usuario Administrador'
        verbose_name_plural = 'Usuarios Administradores'

    def __str__(self):
        return f"{self.usuario} - {self.nombre}"