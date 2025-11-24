from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Medico, Enfermera, Recepcionista, Paciente, Cita, RecetaMedica, HistoriaClinica, SignosVitales
from datetime import date

# Formulario de Login con RUT
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='RUT',
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


# Formulario para crear usuarios (solo para administradores)
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['rut', 'nombre', 'email', 'telefono', 'rol']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }


# Formulario para editar usuarios
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'email', 'telefono', 'rol', 'is_active']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Formularios para Médico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad', 'numero_registro', 'anos_experiencia', 'horario_atencion']
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'anos_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'horario_atencion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lun-Vie 09:00-17:00'}),
        }


# Formulario para Enfermera
class EnfermeraForm(forms.ModelForm):
    class Meta:
        model = Enfermera
        fields = ['numero_registro', 'turno', 'area_asignada']
        widgets = {
            'numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'area_asignada': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulario para Recepcionista
class RecepcionistaForm(forms.ModelForm):
    class Meta:
        model = Recepcionista
        fields = ['area_trabajo', 'horario']
        widgets = {
            'area_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lun-Vie 08:00-16:00'}),
        }


# Formulario de Paciente
class PacienteForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha de Nacimiento'
    )
    
    class Meta:
        model = Paciente
        fields = [
            'rut', 'nombre', 'fecha_nacimiento', 'genero', 'direccion',
            'telefono', 'email', 'contacto_emergencia', 'telefono_emergencia'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del contacto'}),
            'telefono_emergencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56987654321'}),
        }


# Formulario de Historia Clínica
class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = [
            'paciente', 'grupo_sanguineo', 'alergias', 'enfermedades_cronicas',
            'medicamentos_actuales', 'observaciones'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'grupo_sanguineo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: O+, A-, AB+'}),
            'alergias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describa las alergias conocidas'}),
            'enfermedades_cronicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enfermedades crónicas'}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medicamentos que toma actualmente'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }


# Formulario de Cita
class CitaForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='Fecha y Hora'
    )
    
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha_hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo de la consulta'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo médicos activos
        self.fields['medico'].queryset = Medico.objects.filter(activo=True)
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)


# Formulario para actualizar cita (médico)
class CitaMedicoForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['estado', 'diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Diagnóstico detallado'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tratamiento prescrito'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }


# Formulario de Receta Médica
class RecetaMedicaForm(forms.ModelForm):
    vigencia = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Vigencia hasta'
    )
    
    class Meta:
        model = RecetaMedica
        fields = ['cita', 'paciente', 'medicamentos', 'indicaciones', 'vigencia']
        widgets = {
            'cita': forms.Select(attrs={'class': 'form-select'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medicamentos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Liste los medicamentos con dosis y frecuencia. Ej:\n- Paracetamol 500mg - 1 comprimido cada 8 horas\n- Ibuprofeno 400mg - 1 comprimido cada 12 horas'
            }),
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Indicaciones para el paciente'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        medico = kwargs.pop('medico', None)
        super().__init__(*args, **kwargs)
        
        if medico:
            # Filtrar solo las citas del médico
            self.fields['cita'].queryset = Cita.objects.filter(medico=medico)


# Formulario de Signos Vitales
class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        fields = [
            'paciente', 'cita', 'presion_arterial', 'frecuencia_cardiaca',
            'temperatura', 'frecuencia_respiratoria', 'saturacion_oxigeno',
            'peso', 'altura', 'observaciones'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'cita': forms.Select(attrs={'class': 'form-select'}),
            'presion_arterial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '120/80'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '36.5'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '16'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '98'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '70.5'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '170'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
