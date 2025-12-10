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


# Modelo de Médico (extendido del usuario)
class Medico(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='medico')
    especialidad = models.CharField(max_length=100, verbose_name='Especialidad')
    numero_registro = models.CharField(max_length=50, verbose_name='Número de Registro Profesional', unique=True)
    anos_experiencia = models.IntegerField(verbose_name='Años de Experiencia', default=0)
    
    # Configuración de horarios (bloques de 30 minutos)
    duracion_consulta = models.IntegerField(default=30, verbose_name='Duración de Consulta (minutos)')
    
    # Horario mañana
    atiende_manana = models.BooleanField(default=True, verbose_name='Atiende en la mañana')
    hora_inicio_manana = models.TimeField(default='08:30', verbose_name='Hora Inicio Mañana')
    hora_fin_manana = models.TimeField(default='12:30', verbose_name='Hora Fin Mañana')
    
    # Horario tarde
    atiende_tarde = models.BooleanField(default=True, verbose_name='Atiende en la tarde')
    hora_inicio_tarde = models.TimeField(default='13:30', verbose_name='Hora Inicio Tarde')
    hora_fin_tarde = models.TimeField(default='17:00', verbose_name='Hora Fin Tarde')
    
    # Días de atención (1=Lunes, 7=Domingo)
    dias_atencion = models.CharField(
        max_length=20, 
        default='1,2,3,4,5',
        verbose_name='Días de Atención',
        help_text='Días separados por comas (1=Lunes, 2=Martes, etc.)'
    )
    
    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        ordering = ['usuario__nombre']
    
    def __str__(self):
        return f"Dr(a). {self.usuario.nombre} - {self.especialidad}"
    
    def get_dias_atencion_list(self):
        """Retorna lista de días como enteros"""
        return [int(d.strip()) for d in self.dias_atencion.split(',') if d.strip()]
    
    def genera_bloques_horarios(self, fecha):
        """Genera todos los bloques de horarios disponibles para una fecha"""
        from datetime import datetime, timedelta, time
        
        # Verificar si el médico atiende ese día (1=Lunes, 7=Domingo)
        dia_semana = fecha.isoweekday()
        if dia_semana not in self.get_dias_atencion_list():
            return []
        
        bloques = []
        
        # Generar bloques de la mañana
        if self.atiende_manana:
            hora_actual = datetime.combine(fecha, self.hora_inicio_manana)
            hora_fin = datetime.combine(fecha, self.hora_fin_manana)
            
            while hora_actual < hora_fin:
                bloques.append(hora_actual.time())
                hora_actual += timedelta(minutes=self.duracion_consulta)
        
        # Generar bloques de la tarde
        if self.atiende_tarde:
            hora_actual = datetime.combine(fecha, self.hora_inicio_tarde)
            hora_fin = datetime.combine(fecha, self.hora_fin_tarde)
            
            while hora_actual < hora_fin:
                bloques.append(hora_actual.time())
                hora_actual += timedelta(minutes=self.duracion_consulta)
        
        return bloques
    
    def obtener_horarios_disponibles(self, fecha):
        """Obtiene horarios disponibles (no ocupados) para una fecha"""
        from datetime import datetime, time
        
        bloques = self.genera_bloques_horarios(fecha)
        
        # Obtener citas ya agendadas para ese día
        inicio_dia = datetime.combine(fecha, time.min)
        fin_dia = datetime.combine(fecha, time.max)
        
        citas_ocupadas = Cita.objects.filter(
            medico=self,
            fecha_hora__range=(inicio_dia, fin_dia),
            estado__in=['pendiente', 'confirmada', 'en_curso']
        ).values_list('fecha_hora', flat=True)
        
        # Convertir a time para comparar
        horas_ocupadas = [c.time() for c in citas_ocupadas]
        
        # Filtrar bloques ocupados
        horarios_disponibles = [b for b in bloques if b not in horas_ocupadas]
        
        return horarios_disponibles


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
    
    class Meta:
        verbose_name = 'Recepcionista'
        verbose_name_plural = 'Recepcionistas'
        ordering = ['usuario__nombre']
    
    def __str__(self):
        return f"{self.usuario.nombre} - {self.area_trabajo}"
    
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
        # Restricción: un médico no puede tener dos citas al mismo tiempo
        constraints = [
            models.UniqueConstraint(
                fields=['medico', 'fecha_hora'],
                condition=models.Q(estado__in=['pendiente', 'confirmada', 'en_curso']),
                name='unique_medico_fecha_hora_activa'
            )
        ]
    
    def __str__(self):
        return f"Cita: {self.paciente.nombre} - {self.medico} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"


# Modelo de Receta Médica
class RecetaMedica(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.SET_NULL, related_name='recetas', null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recetas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='recetas_emitidas')
    indicaciones = models.TextField(verbose_name='Indicaciones Preventivas')
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
        return f"Signos Vitales - {self.paciente.nombre} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"


# Modelo de Medicamento para Inventario
class Medicamento(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Medicamento')
    gramos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Gramos/Miligramos', help_text='Concentración del medicamento')
    cantidad = models.IntegerField(verbose_name='Cantidad en Stock', default=0)
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.gramos}g (Stock: {self.cantidad})"
    
    def tiene_stock(self):
        """Verifica si hay stock disponible"""
        return self.cantidad > 0
    
    def descontar_stock(self, cantidad):
        """Descuenta cantidad del stock"""
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
            self.save()
            return True
        return False


# Modelo de Relación entre Receta y Medicamentos
class RecetaMedicamento(models.Model):
    receta = models.ForeignKey(RecetaMedica, on_delete=models.CASCADE, related_name='medicamentos_recetados')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='recetas')
    cantidad_recetada = models.IntegerField(verbose_name='Cantidad Recetada', default=1)
    dosis = models.CharField(max_length=200, verbose_name='Dosis', help_text='Ej: 1 comprimido cada 8 horas')
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Medicamento en Receta'
        verbose_name_plural = 'Medicamentos en Recetas'
    
    def __str__(self):
        return f"{self.medicamento.nombre} - Cantidad: {self.cantidad_recetada}"
    
    def save(self, *args, **kwargs):
        """Al guardar, descuenta el stock automáticamente"""
        if not self.pk:  # Solo si es nuevo
            self.medicamento.descontar_stock(self.cantidad_recetada)
        super().save(*args, **kwargs)