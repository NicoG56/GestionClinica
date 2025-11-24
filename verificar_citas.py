import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clinica.settings')
django.setup()

from gestor_app.models import Cita, Medico, CustomUser

print("\n=== Verificando Citas ===\n")

# Verificar médicos
medicos = Medico.objects.all()
print(f"Total médicos en el sistema: {medicos.count()}")
for medico in medicos:
    print(f"  - {medico.usuario.nombre} ({medico.especialidad})")

print("\n=== Citas en el sistema ===\n")
citas = Cita.objects.all()
print(f"Total citas: {citas.count()}")

for cita in citas:
    print(f"\nCita #{cita.id}:")
    print(f"  Paciente: {cita.paciente.nombre}")
    print(f"  Médico: {cita.medico}")
    print(f"  Tipo médico: {type(cita.medico)}")
    print(f"  Fecha: {cita.fecha_hora}")
    print(f"  Estado: {cita.estado}")
