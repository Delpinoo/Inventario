from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, ValidationError, _
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_sucursal =models.CharField(max_length=100)
    direccion= models.CharField(max_length=200)
    telefono = models.CharField( max_length=50)

    def __str__(self):
        return self.nombre_sucursal
    

class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    @property
    def cantidad(self):
        """ Calcula la suma de las cantidades de los productos de este tipo """
        return self.productos.aggregate(total=models.Sum('cantidad'))['total'] or 0

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=0)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True ,related_name="productos")
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='productos')
    
    def __str__(self):
        return self.nombre


class Telefono(models.Model):
    nombre_dueño = models.CharField(max_length=100)
    modelo_telefono = models.CharField(max_length=100)
    fono = models.CharField(max_length=10, validators=[RegexValidator(regex=r'^9\s\d{8}$')])
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='telefonos')
    
    def __str__(self):
        return self.nombre_dueño


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Encripta la contraseña correctamente
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    run = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "run"]

    def __str__(self):
        return self.nombre