import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clinica.settings')
django.setup()

from gestor_app.models import (
    CustomUser, Medico, Enfermera, Recepcionista,
    Paciente, HistoriaClinica, Cita, RecetaMedica, SignosVitales
)

print("\n" + "="*60)
print(" CREANDO DATOS DE PRUEBA - SISTEMA GESTIÓN CLÍNICA")
print("="*60 + "\n")

# ====================  CREAR USUARIOS Y PERFILES ====================
print("1. Creando usuarios y perfiles profesionales...")

# Crear Usuario Médico
try:
    usuario_medico = CustomUser.objects.create_user(
        rut='22222222-2',
        password='medico123',
        nombre='Dr. Carlos Ramírez',
        email='carlos.ramirez@clinica.cl',
        telefono='+56987654321',
        rol='medico'
    )
    medico = Medico.objects.create(
        usuario=usuario_medico,
        especialidad='Medicina General',
        numero_registro='MED-2024-001',
        anos_experiencia=10,
        horario_atencion='Lun-Vie: 09:00-17:00'
    )
    print(f"   ✓ Médico creado: {medico}")
except Exception as e:
    print(f"   ✗ Error creando médico: {e}")
    medico = Medico.objects.filter(usuario__rut='22222222-2').first()

# Crear Usuario Enfermera
try:
    usuario_enfermera = CustomUser.objects.create_user(
        rut='33333333-3',
        password='enfermera123',
        nombre='María González',
        email='maria.gonzalez@clinica.cl',
        telefono='+56965432109',
        rol='enfermera'
    )
    enfermera = Enfermera.objects.create(
        usuario=usuario_enfermera,
        numero_registro='ENF-2024-001',
        turno='manana',
        area_asignada='Consulta Externa'
    )
    print(f"   ✓ Enfermera creada: {enfermera}")
except Exception as e:
    print(f"   ✗ Error creando enfermera: {e}")
    enfermera = Enfermera.objects.filter(usuario__rut='33333333-3').first()

# Crear Usuario Recepcionista
try:
    usuario_recepcionista = CustomUser.objects.create_user(
        rut='44444444-4',
        password='recepcionista123',
        nombre='Ana Torres',
        email='ana.torres@clinica.cl',
        telefono='+56943210987',
        rol='recepcionista'
    )
    recepcionista = Recepcionista.objects.create(
        usuario=usuario_recepcionista,
        area_trabajo='Recepción Principal',
        horario='Lun-Vie: 08:00-16:00'
    )
    print(f"   ✓ Recepcionista creada: {recepcionista}")
except Exception as e:
    print(f"   ✗ Error creando recepcionista: {e}")
    recepcionista = Recepcionista.objects.filter(usuario__rut='44444444-4').first()

# ==================== CREAR PACIENTES ====================
print("\n2. Creando pacientes...")

pacientes_data = [
    {
        'rut': '15555555-5',
        'nombre': 'Juan Pérez López',
        'fecha_nacimiento': '1985-03-15',
        'genero': 'M',
        'direccion': 'Av. Principal 123, Santiago',
        'telefono': '+56912345678',
        'email': 'juan.perez@email.com',
        'contacto_emergencia': 'María Pérez (Hermana)',
        'telefono_emergencia': '+56923456789'
    },
    {
        'rut': '16666666-6',
        'nombre': 'Carmen Silva Rojas',
        'fecha_nacimiento': '1990-07-22',
        'genero': 'F',
        'direccion': 'Calle Los Álamos 456, Providencia',
        'telefono': '+56934567890',
        'email': 'carmen.silva@email.com',
        'contacto_emergencia': 'Pedro Silva (Esposo)',
        'telefono_emergencia': '+56945678901'
    },
    {
        'rut': '17777777-7',
        'nombre': 'Roberto Fernández Muñoz',
        'fecha_nacimiento': '1975-11-08',
        'genero': 'M',
        'direccion': 'Pasaje Los Robles 789, Las Condes',
        'telefono': '+56956789012',
        'email': 'roberto.fernandez@email.com',
        'contacto_emergencia': 'Laura Muñoz (Esposa)',
        'telefono_emergencia': '+56967890123'
    }
]

pacientes = []
for data in pacientes_data:
    try:
        paciente, created = Paciente.objects.get_or_create(
            rut=data['rut'],
            defaults=data
        )
        if created:
            print(f"   ✓ Paciente creado: {paciente.nombre}")
        else:
            print(f"   ○ Paciente ya existía: {paciente.nombre}")
        pacientes.append(paciente)
    except Exception as e:
        print(f"   ✗ Error creando paciente {data['nombre']}: {e}")

# ==================== CREAR HISTORIAS CLÍNICAS ====================
print("\n3. Creando historias clínicas...")

admin = CustomUser.objects.filter(rol='administrador').first()

historias_data = [
    {
        'paciente': pacientes[0],
        'grupo_sanguineo': 'O+',
        'alergias': 'Penicilina',
        'enfermedades_cronicas': 'Hipertensión arterial controlada',
        'medicamentos_actuales': 'Losartán 50mg - 1 vez al día',
        'observaciones': 'Paciente con seguimiento regular'
    },
    {
        'paciente': pacientes[1],
        'grupo_sanguineo': 'A-',
        'alergias': 'Ninguna conocida',
        'enfermedades_cronicas': 'Ninguna',
        'medicamentos_actuales': 'No consume medicamentos regulares',
        'observaciones': 'Paciente sana'
    },
    {
        'paciente': pacientes[2],
        'grupo_sanguineo': 'B+',
        'alergias': 'Aspirina',
        'enfermedades_cronicas': 'Diabetes tipo 2',
        'medicamentos_actuales': 'Metformina 850mg - 2 veces al día',
        'observaciones': 'Control mensual de glicemia'
    }
]

for historia_data in historias_data:
    try:
        historia, created = HistoriaClinica.objects.get_or_create(
            paciente=historia_data['paciente'],
            defaults={
                **historia_data,
                'actualizado_por': admin
            }
        )
        if created:
            print(f"   ✓ Historia clínica creada para: {historia.paciente.nombre}")
        else:
            print(f"   ○ Historia clínica ya existía para: {historia.paciente.nombre}")
    except Exception as e:
        print(f"   ✗ Error creando historia clínica: {e}")

# ==================== CREAR CITAS ====================
print("\n4. Creando citas médicas...")

if medico:
    ahora = timezone.now()
    
    citas_data = [
        {
            'paciente': pacientes[0],
            'fecha_hora': ahora + timedelta(hours=2),
            'motivo': 'Control de presión arterial',
            'estado': 'confirmada',
            'observaciones': 'Traer resultados de exámenes'
        },
        {
            'paciente': pacientes[1],
            'fecha_hora': ahora + timedelta(days=1, hours=10),
            'motivo': 'Consulta por dolor de cabeza',
            'estado': 'pendiente',
            'observaciones': ''
        },
        {
            'paciente': pacientes[2],
            'fecha_hora': ahora - timedelta(days=1),
            'motivo': 'Control de diabetes',
            'estado': 'completada',
            'diagnostico': 'Diabetes tipo 2 controlada. Glicemia en rango normal.',
            'tratamiento': 'Continuar con tratamiento actual. Control en 1 mes.'
        }
    ]
    
    citas = []
    for cita_data in citas_data:
        try:
            cita, created = Cita.objects.get_or_create(
                paciente=cita_data['paciente'],
                medico=medico,
                fecha_hora=cita_data['fecha_hora'],
                defaults={
                    **cita_data,
                    'creada_por': usuario_recepcionista if recepcionista else admin
                }
            )
            if created:
                print(f"   ✓ Cita creada: {cita.paciente.nombre} - {cita.get_estado_display()}")
            else:
                print(f"   ○ Cita ya existía: {cita.paciente.nombre}")
            citas.append(cita)
        except Exception as e:
            print(f"   ✗ Error creando cita: {e}")
else:
    print("   ✗ No se encontró médico para crear citas")
    citas = []

# ==================== CREAR SIGNOS VITALES ====================
print("\n5. Registrando signos vitales...")

if enfermera and len(citas) > 0:
    for i, cita in enumerate(citas[:2]):  # Solo para las primeras 2 citas
        try:
            signos, created = SignosVitales.objects.get_or_create(
                paciente=cita.paciente,
                cita=cita,
                defaults={
                    'enfermera': enfermera,
                    'presion_arterial': ['120/80', '115/75', '130/85'][i % 3],
                    'frecuencia_cardiaca': [72, 68, 78][i % 3],
                    'temperatura': 36.5 + (i * 0.2),
                    'frecuencia_respiratoria': [16, 18, 17][i % 3],
                    'saturacion_oxigeno': [98, 97, 99][i % 3],
                    'peso': 70.5 + (i * 5),
                    'altura': 170 + (i * 3),
                    'observaciones': 'Signos vitales dentro de parámetros normales'
                }
            )
            if created:
                print(f"   ✓ Signos vitales registrados para: {signos.paciente.nombre}")
            else:
                print(f"   ○ Signos vitales ya existían para: {signos.paciente.nombre}")
        except Exception as e:
            print(f"   ✗ Error registrando signos vitales: {e}")
else:
    print("   ✗ No se encontró enfermera o citas para registrar signos vitales")

# ==================== CREAR RECETA MÉDICA ====================
print("\n6. Creando recetas médicas...")

if medico and len(citas) > 2 and citas[2].estado == 'completada':
    try:
        receta, created = RecetaMedica.objects.get_or_create(
            cita=citas[2],
            paciente=citas[2].paciente,
            medico=medico,
            defaults={
                'medicamentos': '''- Metformina 850mg - 1 comprimido cada 12 horas (desayuno y cena)
- Atorvastatina 20mg - 1 comprimido en la noche
- Ácido Acetilsalicílico 100mg - 1 comprimido en la mañana''',
                'indicaciones': '''- Tomar con alimentos
- No suspender tratamiento sin consultar
- Control en 30 días con exámenes de glicemia y perfil lipídico
- Mantener dieta baja en azúcares y grasas
- Realizar ejercicio físico moderado 30 min diarios''',
                'vigencia': timezone.now().date() + timedelta(days=30)
            }
        )
        if created:
            print(f"   ✓ Receta creada para: {receta.paciente.nombre}")
        else:
            print(f"   ○ Receta ya existía para: {receta.paciente.nombre}")
    except Exception as e:
        print(f"   ✗ Error creando receta: {e}")
else:
    print("   ○ No se creó receta (se requiere cita completada)")

# ==================== RESUMEN ====================
print("\n" + "="*60)
print(" RESUMEN DE DATOS CREADOS")
print("="*60)
print(f"\n📊 Estadísticas:")
print(f"   • Usuarios: {CustomUser.objects.count()}")
print(f"   • Médicos: {Medico.objects.count()}")
print(f"   • Enfermeras: {Enfermera.objects.count()}")
print(f"   • Recepcionistas: {Recepcionista.objects.count()}")
print(f"   • Pacientes: {Paciente.objects.count()}")
print(f"   • Historias Clínicas: {HistoriaClinica.objects.count()}")
print(f"   • Citas: {Cita.objects.count()}")
print(f"   • Recetas: {RecetaMedica.objects.count()}")
print(f"   • Registros de Signos Vitales: {SignosVitales.objects.count()}")

print(f"\n🔐 Credenciales de acceso:")
print(f"\n   Administrador:")
print(f"   • RUT: 11111111-1")
print(f"   • Contraseña: admin123")
print(f"\n   Médico:")
print(f"   • RUT: 22222222-2")
print(f"   • Contraseña: medico123")
print(f"\n   Enfermera:")
print(f"   • RUT: 33333333-3")
print(f"   • Contraseña: enfermera123")
print(f"\n   Recepcionista:")
print(f"   • RUT: 44444444-4")
print(f"   • Contraseña: recepcionista123")

print("\n" + "="*60)
print(" ✓ PROCESO COMPLETADO")
print("="*60 + "\n")
