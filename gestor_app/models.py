from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Manager personalizado para el usuario
class CustomUserManager(BaseUserManager):
    def create_user(self, rut, password=None, **extra_fields):
        if not rut:
            raise ValueError('El RUT es obligatorio')
        user = self.model(rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'administrador')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(rut, password, **extra_fields)

# Modelo de Usuario Personalizado (Base para autenticación)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('administrador', 'Administrador'),
        ('medico', 'Médico'),
        ('enfermera', 'Enfermera'),
        ('recepcionista', 'Recepcionista'),
    )
    
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dkK]$',
        message='El RUT debe estar en formato: 12345678-9'
    )
    
    rut = models.CharField(max_length=12, unique=True, validators=[rut_validator], verbose_name='RUT')
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['nombre']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombre} ({self.rut}) - {self.get_rol_display()}"
    
    def es_administrador(self):
        return self.rol == 'administrador'
    
    def es_medico(self):
        return self.rol == 'medico' or hasattr(self, 'medico')
    
    def es_enfermera(self):
        return self.rol == 'enfermera' or hasattr(self, 'enfermera')
    
    def es_recepcionista(self):
        return self.rol == 'recepcionista' or hasattr(self, 'recepcionista')


# Modelo de Médico (extendido del usuario)
class Medico(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='medico')
    especialidad = models.CharField(max_length=100, verbose_name='Especialidad')
    numero_registro = models.CharField(max_length=50, verbose_name='Número de Registro Profesional', unique=True)
    anos_experiencia = models.IntegerField(verbose_name='Años de Experiencia', default=0)
    horario_atencion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Horario de Atención')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['usuario__nombre']
    
    def __str__(self):
        return f"Dr(a). {self.usuario.nombre} - {self.especialidad}"


# Modelo de Enfermera (extendido del usuario)
class Enfermera(models.Model):
    TURNO_CHOICES = (
        ('manana', 'Mañana (08:00-16:00)'),
        ('tarde', 'Tarde (16:00-00:00)'),
        ('noche', 'Noche (00:00-08:00)'),
    )
    
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='enfermera')
    numero_registro = models.CharField(max_length=50, verbose_name='Número de Registro Profesional', unique=True)
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES, default='manana')
    area_asignada = models.CharField(max_length=100, blank=True, null=True, verbose_name='Área Asignada')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Enfermera'
        verbose_name_plural = 'Enfermeras'
        ordering = ['usuario__nombre']
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.get_turno_display()}"


# Modelo de Recepcionista (extendido del usuario)
class Recepcionista(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recepcionista')
    area_trabajo = models.CharField(max_length=100, verbose_name='Área de Trabajo', default='Recepción General')
    horario = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Recepcionista'
        verbose_name_plural = 'Recepcionistas'
        ordering = ['usuario__nombre']
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.area_trabajo}"


# Modelo de Paciente
class Paciente(models.Model):
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )
    
    rut = models.CharField(max_length=12, unique=True, verbose_name='RUT')
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=100, verbose_name='Contacto de Emergencia')
    telefono_emergencia = models.CharField(max_length=15, verbose_name='Teléfono de Emergencia')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.rut})"


# Modelo de Historia Clínica
class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historia')
    grupo_sanguineo = models.CharField(max_length=5, blank=True, null=True, verbose_name='Grupo Sanguíneo')
    alergias = models.TextField(blank=True, null=True)
    enfermedades_cronicas = models.TextField(blank=True, null=True, verbose_name='Enfermedades Crónicas')
    medicamentos_actuales = models.TextField(blank=True, null=True, verbose_name='Medicamentos Actuales')
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='historias_actualizadas')
    
    class Meta:
        verbose_name = 'Historia Clínica'
        verbose_name_plural = 'Historias Clínicas'
    
    def __str__(self):
        return f"Historia Clínica de {self.paciente.nombre}"


# Modelo de Cita Médica
class Cita(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField(verbose_name='Fecha y Hora')
    motivo = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True, verbose_name='Diagnóstico')
    tratamiento = models.TextField(blank=True, null=True)
    creada_por = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='citas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cita Médica'
        verbose_name_plural = 'Citas Médicas'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"Cita: {self.paciente.nombre} - {self.medico} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"


# Modelo de Receta Médica
class RecetaMedica(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='recetas')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='recetas_emitidas')
    medicamentos = models.TextField(verbose_name='Medicamentos (detalle, dosis y frecuencia)')
    indicaciones = models.TextField()
    fecha_emision = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')
    vigencia = models.DateField(verbose_name='Vigencia hasta')
    
    class Meta:
        verbose_name = 'Receta Médica'
        verbose_name_plural = 'Recetas Médicas'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Receta para {self.paciente.nombre} - {self.medico} ({self.fecha_emision.strftime('%d/%m/%Y')})"


# Modelo de Registro de Signos Vitales (para enfermeras)
class SignosVitales(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='signos_vitales')
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='signos_vitales', null=True, blank=True)
    enfermera = models.ForeignKey(Enfermera, on_delete=models.SET_NULL, null=True, related_name='signos_registrados')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    presion_arterial = models.CharField(max_length=10, verbose_name='Presión Arterial (ej: 120/80)')
    frecuencia_cardiaca = models.IntegerField(verbose_name='Frecuencia Cardíaca (lpm)')
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Temperatura (°C)')
    frecuencia_respiratoria = models.IntegerField(verbose_name='Frecuencia Respiratoria (rpm)')
    saturacion_oxigeno = models.IntegerField(verbose_name='Saturación de Oxígeno (%)')
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)', blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Altura (cm)', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Registro de Signos Vitales'
        verbose_name_plural = 'Registros de Signos Vitales'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"Signos Vitales de {self.paciente.nombre} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
