import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clinica.settings')
django.setup()

from gestor_app.models import CustomUser

# Verificar usuario recepcionista
try:
    recep = CustomUser.objects.get(rut='44444444-4')
    print(f"Usuario encontrado: {recep.nombre}")
    print(f"RUT: {recep.rut}")
    print(f"Rol: {recep.rol}")
    print(f"Is authenticated: True (si puede hacer login)")
    print(f"Is active: {recep.is_active}")
    
    # Verificar permisos
    print(f"\nVerificación de función puede_gestionar_pacientes:")
    print(f"user.is_authenticated: True")
    print(f"user.rol: '{recep.rol}'")
    print(f"user.rol in ['administrador', 'medico', 'enfermera', 'recepcionista']: {recep.rol in ['administrador', 'medico', 'enfermera', 'recepcionista']}")
    
    # Verificar si tiene perfil Recepcionista
    try:
        perfil = recep.recepcionista
        print(f"\nPerfil Recepcionista encontrado:")
        print(f"  Área: {perfil.area_trabajo}")
        print(f"  Activo: {perfil.activo}")
    except Exception as e:
        print(f"\n⚠️ No tiene perfil Recepcionista asociado: {e}")
        
except CustomUser.DoesNotExist:
    print("❌ Usuario recepcionista no encontrado")
