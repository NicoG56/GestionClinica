# Sistema de Gestión Clínica

Sistema de gestión clínica desarrollado en Django con control de acceso por roles (Administrador, Médico, Enfermera, Recepcionista). Incluye gestión de pacientes, citas médicas, historias clínicas, recetas médicas con inventario de medicamentos, y signos vitales.

## Requisitos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip

## Instalación Rápida (Paso a Paso)

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
pip install django mysqlclient reportlab
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

**Credenciales creadas:**
- **RUT:** 11111111-1
- **Contraseña:** admin123

### 8. Iniciar el servidor
```bash
python manage.py runserver
```

**Acceder en:** http://127.0.0.1:8000/

## Credenciales de Acceso

**Administrador:**
- RUT: 11111111-1
- Contraseña: admin123

## Funcionalidades por Rol

### 👨‍💼 Administrador
- Gestión completa de usuarios del sistema (crear, editar, eliminar)
- Gestión de pacientes y edición de datos personales
- Gestión de inventario de medicamentos (agregar, actualizar stock, eliminar)
- Ver estadísticas del sistema
- Acceso completo a todas las funcionalidades

### 👨‍⚕️ Médico
- Ver información completa de pacientes
- Gestionar antecedentes patológicos de pacientes
- Emitir recetas médicas con medicamentos del inventario
- Generar recetas en PDF
- Ver y agregar observaciones a citas del día
- Gestionar sus propias citas (próximas 5 días)
- Ver historial de consultas de pacientes

### 👩‍⚕️ Enfermera
- Registrar signos vitales de pacientes
- Ver citas del día y próximas citas (5 días)
- Ver información de pacientes (solo lectura)
- Consultar historias clínicas

### 🧑‍💼 Recepcionista
- Gestión de pacientes (crear, editar, consultar)
- Agendar citas médicas (bloques de 30 minutos)
- Ver disponibilidad de médicos
- Gestionar citas del día

## Características Principales

### 📋 Gestión de Citas
- Sistema de agendamiento en bloques de 30 minutos
- Validación de disponibilidad en tiempo real
- Horarios configurables por médico (mañana/tarde)
- Vista de citas del día en todos los dashboards
- Próximas citas (5 días) para médicos y enfermeras

### 💊 Sistema de Inventario de Medicamentos
- Control de stock en tiempo real
- Descuento automático al emitir recetas
- Búsqueda de medicamentos con stock disponible
- Alertas visuales de stock (bajo/agotado)
- Gestión exclusiva por administrador

### 📝 Recetas Médicas
- Selección de medicamentos desde inventario
- Múltiples medicamentos por receta
- Indicaciones preventivas personalizadas
- Generación automática de PDF
- Fecha de emisión automática
- Control de vigencia

### 📊 Historias Clínicas
- Antecedentes patológicos
- Historial completo de consultas
- Diagnósticos y tratamientos
- Observaciones médicas por cita
- Signos vitales registrados

## Tecnologías

- **Backend:** Django 5.2.8
- **Base de Datos:** MySQL 5.7+
- **Frontend:** Bootstrap 5.3
- **Generación PDF:** ReportLab
- **Timezone:** America/Santiago (UTC-3)

## Estructura Principal

```
gestionClinica/
├── gestion_clinica/         # Configuración del proyecto
│   ├── settings.py         # Configuración general
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── gestor_app/              # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Lógica de negocio
│   ├── forms.py            # Formularios
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Panel de administración
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html
│   │   ├── citas/
│   │   ├── pacientes/
│   │   ├── recetas/
│   │   ├── medicamentos/
│   │   └── ...
│   ├── static/             # Archivos estáticos
│   │   ├── estilos/
│   │   └── img/
│   └── migrations/         # Migraciones de BD
├── manage.py
├── crear_superusuario.py   # Script inicial
└── README.md
```

## Modelos de Datos

- **CustomUser:** Usuarios con roles
- **Paciente:** Información de pacientes
- **Medico / Enfermera / Recepcionista:** Perfiles profesionales
- **Cita:** Citas médicas
- **RecetaMedica:** Recetas emitidas
- **RecetaMedicamento:** Relación receta-medicamento (descuento automático)
- **Medicamento:** Inventario de medicamentos
- **HistoriaClinica:** Antecedentes patológicos
- **SignosVitales:** Registros de signos vitales

## Notas Importantes

- ✅ El RUT debe tener formato: `12345678-9` (con guión y dígito verificador)
- ✅ Solo médicos y administradores pueden editar datos de pacientes
- ✅ Las recetas médicas se descargan automáticamente en PDF
- ✅ El stock de medicamentos se descuenta automáticamente al emitir recetas
- ✅ Sistema configurado para zona horaria de Chile (America/Santiago)

## Solución de Problemas

**Error de conexión a MySQL:**
- Verificar que MySQL esté corriendo
- Validar credenciales en `settings.py`
- Confirmar que existe la base de datos `gestion_db`

**Error en migraciones:**
```bash
python manage.py migrate --run-syncdb
```

**Problemas con zona horaria:**
El sistema usa `America/Santiago` por defecto. Cambiar en `settings.py` si es necesario.

---

**Desarrollado con Django** | Sistema de gestión clínica completo
