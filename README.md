# Sistema de Gestión Clínica

Sistema de gestión clínica desarrollado en Django con control de acceso por roles (Administrador, Médico, Enfermera, Recepcionista). Gestiona pacientes, citas médicas, historias clínicas, recetas médicas y signos vitales.

## 📋 Requisitos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip

## 🚀 Instalación Rápida (Paso a Paso)

### 1. Clonar el repositorio
```bash
git clone https://github.com/NicoG56/GestionClinica.git
cd GestionClinica
```

### 2. Crear y activar entorno virtual
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install django mysqlclient reportlab locust
```

### 4. Crear la base de datos en MySQL
```sql
CREATE DATABASE gestion_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar la base de datos
Editar `gestion_clinica/settings.py` con tus credenciales de MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gestion_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario administrador
```bash
python crear_superusuario.py
```

Credenciales creadas:
- **RUT:** 11111111-1
- **Contraseña:** admin123

### 8. (Opcional) Cargar datos de prueba
```bash
python crear_datos_prueba.py
```

Esto creará usuarios de ejemplo para cada rol con sus pacientes y citas.

### 9. Iniciar el servidor
```bash
python manage.py runserver
```

Acceder en: **http://127.0.0.1:8000/**

## 🧪 Pruebas de Rendimiento

Para ejecutar pruebas de carga con Locust:

### 1. Asegúrate de que el servidor Django esté corriendo
```bash
python manage.py runserver
```

### 2. En otra terminal, ejecuta Locust
```bash
locust --host=http://127.0.0.1:8000
```

### 3. Abrir la interfaz de Locust
Acceder a: **http://localhost:8089**

### 4. Configurar la prueba
- **Number of users:** 10 (o el número deseado)
- **Spawn rate:** 2 (usuarios por segundo)
- Clic en "Start swarming"

Locust simulará usuarios con diferentes roles realizando acciones típicas del sistema (crear pacientes, agendar citas, emitir recetas, etc.).

## 👥 Credenciales de Prueba

Si ejecutaste `crear_datos_prueba.py`, puedes usar:

| Rol | RUT | Contraseña |
|-----|-----|------------|
| Administrador | 11111111-1 | admin123 |
| Recepcionista | 22222222-2 | recep123 |
| Médico | 33333333-3 | medico123 |
| Enfermera | 44444444-4 | enfermera123 |

## 📱 Funcionalidades por Rol

### Administrador
- Crear, editar y eliminar usuarios del sistema
- Editar datos personales de pacientes
- Acceso completo a todas las funcionalidades

### Recepcionista
- Gestión de pacientes (crear, ver)
- Agendar y gestionar citas médicas
- Consultar información

### Médico
- Ver pacientes y sus historias clínicas
- Actualizar diagnósticos y tratamientos
- Emitir recetas médicas (con generación de PDF)
- Gestionar sus propias citas

### Enfermera
- Registrar signos vitales
- Ver citas programadas
- Actualizar historias clínicas

## 🎨 Tecnologías

- **Backend:** Django 5.2.8
- **Base de Datos:** MySQL
- **Frontend:** Bootstrap 5.3
- **PDF:** ReportLab
- **Testing:** Locust

## 📁 Estructura Principal

```
gestionClinica/
├── gestion_clinica/         # Configuración del proyecto
├── gestor_app/              # Aplicación principal
│   ├── models.py           # Modelos: CustomUser, Paciente, Cita, etc.
│   ├── views.py            # Lógica de negocio
│   ├── forms.py            # Formularios
│   ├── templates/          # Plantillas HTML
│   └── static/             # CSS, imágenes
├── manage.py
├── crear_superusuario.py   # Script para crear admin
├── crear_datos_prueba.py   # Script para datos de ejemplo
└── locustfile.py           # Pruebas de rendimiento
```

## ⚠️ Notas Importantes

- El RUT debe tener formato: `12345678-9` (con guión y dígito verificador)
- Solo el administrador puede editar datos personales de pacientes
- Las recetas médicas se pueden descargar en PDF
- Cambiar la contraseña del administrador después del primer login

## 🐛 Solución de Problemas

**Error al instalar mysqlclient:**
```bash
pip install mysqlclient
```

**Error "Table doesn't exist":**
```bash
python manage.py migrate
```

**Error de conexión a MySQL:**
Verificar que MySQL esté corriendo y las credenciales sean correctas.

---

**Desarrollado con Django** | Sistema de gestión clínica educativo
