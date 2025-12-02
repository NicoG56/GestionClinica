from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Medico, Enfermera, Recepcionista, Paciente, Cita, RecetaMedica, HistoriaClinica, SignosVitales

# Admin personalizado para el modelo de usuario
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['rut', 'nombre', 'rol', 'email', 'fecha_creacion']
    list_filter = ['rol', 'is_staff']
    search_fields = ['rut', 'nombre', 'email']
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        (None, {'fields': ('rut', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'email', 'telefono')}),
        ('Rol y Permisos', {'fields': ('rol', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('fecha_creacion', 'last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rut', 'nombre', 'rol', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['fecha_creacion', 'last_login']


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_rut', 'especialidad', 'numero_registro']
    list_filter = ['especialidad']
    search_fields = ['usuario__nombre', 'usuario__rut', 'especialidad', 'numero_registro']
    ordering = ['usuario__nombre']
    
    def get_nombre(self, obj):
        return obj.usuario.nombre
    get_nombre.short_description = 'Nombre'
    
    def get_rut(self, obj):
        return obj.usuario.rut
    get_rut.short_description = 'RUT'


@admin.register(Enfermera)
class EnfermeraAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_rut', 'numero_registro', 'turno']
    list_filter = ['turno']
    search_fields = ['usuario__nombre', 'usuario__rut', 'numero_registro']
    ordering = ['usuario__nombre']
    
    def get_nombre(self, obj):
        return obj.usuario.nombre
    get_nombre.short_description = 'Nombre'
    
    def get_rut(self, obj):
        return obj.usuario.rut
    get_rut.short_description = 'RUT'


@admin.register(Recepcionista)
class RecepcionistaAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_rut', 'area_trabajo']
    list_filter = []
    search_fields = ['usuario__nombre', 'usuario__rut', 'area_trabajo']
    ordering = ['usuario__nombre']
    
    def get_nombre(self, obj):
        return obj.usuario.nombre
    get_nombre.short_description = 'Nombre'
    
    def get_rut(self, obj):
        return obj.usuario.rut
    get_rut.short_description = 'RUT'

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'fecha_nacimiento', 'telefono', 'fecha_registro']
    list_filter = ['genero', 'fecha_registro']
    search_fields = ['rut', 'nombre', 'telefono']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro']


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'grupo_sanguineo', 'actualizado_por', 'fecha_actualizacion']
    list_filter = ['grupo_sanguineo', 'fecha_creacion']
    search_fields = ['paciente__nombre', 'paciente__rut']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha_hora', 'estado', 'creada_por']
    list_filter = ['estado', 'fecha_hora', 'medico']
    search_fields = ['paciente__nombre', 'medico__usuario__nombre', 'motivo']
    ordering = ['-fecha_hora']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(RecetaMedica)
class RecetaMedicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medico', 'fecha_emision', 'vigencia']
    list_filter = ['fecha_emision', 'vigencia', 'medico']
    search_fields = ['paciente__nombre', 'medico__usuario__nombre']
    ordering = ['-fecha_emision']
    readonly_fields = ['fecha_emision']


@admin.register(SignosVitales)
class SignosVitalesAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'enfermera', 'presion_arterial', 'temperatura', 'fecha_hora']
    list_filter = ['fecha_hora', 'enfermera']
    search_fields = ['paciente__nombre', 'enfermera__usuario__nombre']
    ordering = ['-fecha_hora']
    readonly_fields = ['fecha_hora']
