"""
Script para crear el superusuario administrador inicial del sistema
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clinica.settings')
django.setup()

from gestor_app.models import CustomUser

User = CustomUser

# Verificar si ya existe un superusuario
if User.objects.filter(is_superuser=True).exists():
    print("\n" + "=" * 60)
    print("Ya existe un superusuario en el sistema.")
    print("Superusuarios existentes:")
    for user in User.objects.filter(is_superuser=True):
        print(f"  - {user.nombre} ({user.rut}) - {user.get_rol_display()}")
    print("=" * 60 + "\n")
else:
    # Crear el superusuario administrador
    rut = "11111111-1"
    nombre = "Administrador Sistema"
    password = "admin123"
    
    try:
        admin = User.objects.create_superuser(
            rut=rut,
            nombre=nombre,
            password=password
        )
        admin.email = "admin@clinica.cl"
        admin.save()
        
        print("\n" + "=" * 60)
        print("    SUPERUSUARIO CREADO EXITOSAMENTE")
        print("=" * 60)
        print(f"RUT:        {rut}")
        print(f"Nombre:     {nombre}")
        print(f"Contraseña: {password}")
        print(f"Rol:        Administrador")
        print("=" * 60)
        print("IMPORTANTE: Cambie la contraseña después del primer login")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\nError al crear superusuario: {e}\n")
