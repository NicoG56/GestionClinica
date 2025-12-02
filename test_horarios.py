"""
Script de prueba para verificar el sistema de horarios
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clinica.settings')
django.setup()

from gestor_app.models import Medico, Cita, Paciente, CustomUser
from datetime import datetime, date, timedelta

def test_horarios():
    print("=" * 60)
    print("PRUEBA DEL SISTEMA DE HORARIOS")
    print("=" * 60)
    
    # Obtener un médico (o crear uno de prueba)
    medicos = Medico.objects.all()
    if not medicos.exists():
        print("\n❌ No hay médicos en el sistema. Cree uno primero.")
        return
    
    medico = medicos.first()
    print(f"\n✓ Médico: {medico.usuario.nombre}")
    print(f"  Especialidad: {medico.especialidad}")
    print(f"  Duración consulta: {medico.duracion_consulta} minutos")
    
    # Fecha de prueba (mañana)
    fecha_prueba = date.today() + timedelta(days=1)
    print(f"\n📅 Fecha de prueba: {fecha_prueba}")
    
    # Generar bloques de horarios
    bloques = medico.genera_bloques_horarios(fecha_prueba)
    print(f"\n🕐 Bloques generados: {len(bloques)}")
    if bloques:
        print(f"   Primer bloque: {bloques[0]}")
        print(f"   Último bloque: {bloques[-1]}")
    
    # Obtener horarios disponibles
    disponibles = medico.obtener_horarios_disponibles(fecha_prueba)
    print(f"\n✓ Horarios disponibles: {len(disponibles)}")
    
    # Mostrar citas existentes para esa fecha
    inicio_dia = datetime.combine(fecha_prueba, datetime.min.time())
    fin_dia = datetime.combine(fecha_prueba, datetime.max.time())
    
    citas_dia = Cita.objects.filter(
        medico=medico,
        fecha_hora__range=(inicio_dia, fin_dia),
        estado__in=['pendiente', 'confirmada', 'en_curso']
    )
    
    print(f"\n📋 Citas agendadas para ese día: {citas_dia.count()}")
    for cita in citas_dia:
        print(f"   - {cita.fecha_hora.strftime('%H:%M')} - {cita.paciente.nombre} ({cita.estado})")
    
    # Mostrar algunos horarios disponibles
    if disponibles:
        print(f"\n✅ Primeros 5 horarios disponibles:")
        for hora in disponibles[:5]:
            print(f"   - {hora.strftime('%H:%M')}")
    else:
        print("\n⚠️ No hay horarios disponibles")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == '__main__':
    test_horarios()
