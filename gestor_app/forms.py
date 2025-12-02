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
        fields = ['nombre', 'email', 'telefono', 'rol']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }


# Formularios para Médico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            'especialidad', 'numero_registro', 'anos_experiencia', 'duracion_consulta',
            'atiende_manana', 'hora_inicio_manana', 'hora_fin_manana',
            'atiende_tarde', 'hora_inicio_tarde', 'hora_fin_tarde', 'dias_atencion'
        ]
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'anos_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'duracion_consulta': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'atiende_manana': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hora_inicio_manana': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin_manana': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'atiende_tarde': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hora_inicio_tarde': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin_tarde': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dias_atencion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '1,2,3,4,5 (1=Lun, 2=Mar, ..., 7=Dom)'
            }),
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


# Formulario para crear/editar citas
class CitaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha',
        required=True
    )
    
    hora = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Hora',
        required=True
    )
    
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'motivo', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo de la consulta'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando una cita existente, cargar sus horarios
        if self.instance and self.instance.pk:
            medico = self.instance.medico
            fecha = self.instance.fecha_hora.date()
            hora_actual = self.instance.fecha_hora.time()
            
            # Obtener horarios disponibles
            horarios = medico.obtener_horarios_disponibles(fecha)
            
            # Agregar la hora actual si no está en la lista (porque está ocupada por esta cita)
            if hora_actual not in horarios:
                horarios.append(hora_actual)
                horarios.sort()
            
            self.fields['hora'].choices = [(h.strftime('%H:%M'), h.strftime('%H:%M')) for h in horarios]
            self.fields['fecha'].initial = fecha
            self.fields['hora'].initial = hora_actual.strftime('%H:%M')
        else:
            # Para nueva cita, cargar horarios si hay datos POST
            if 'medico' in self.data and 'fecha' in self.data:
                try:
                    from datetime import datetime
                    medico = Medico.objects.get(id=self.data.get('medico'))
                    fecha = datetime.strptime(self.data.get('fecha'), '%Y-%m-%d').date()
                    horarios = medico.obtener_horarios_disponibles(fecha)
                    self.fields['hora'].choices = [(h.strftime('%H:%M'), h.strftime('%H:%M')) for h in horarios]
                except (Medico.DoesNotExist, ValueError):
                    self.fields['hora'].choices = [('', 'Error al cargar horarios')]
            else:
                self.fields['hora'].choices = [('', 'Primero seleccione médico y fecha')]
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        medico = cleaned_data.get('medico')
        
        if fecha and hora and medico:
            from datetime import datetime
            
            # Convertir hora string a time
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            
            # Combinar fecha y hora
            fecha_hora = datetime.combine(fecha, hora_obj)
            cleaned_data['fecha_hora'] = fecha_hora
            
            # Validar que el horario esté disponible
            cita_existente = Cita.objects.filter(
                medico=medico,
                fecha_hora=fecha_hora,
                estado__in=['pendiente', 'confirmada', 'en_curso']
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if cita_existente.exists():
                raise forms.ValidationError('Este horario ya está ocupado. Por favor, seleccione otro.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.fecha_hora = self.cleaned_data['fecha_hora']
        instance.estado = 'pendiente'
        
        if commit:
            instance.save()
        return instance


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
