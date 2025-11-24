# Sistema de Gestión Clínica

Sistema completo de gestión clínica desarrollado en Django que permite administrar pacientes, citas médicas, historias clínicas, recetas médicas y signos vitales con control de acceso basado en roles.

## 🏥 Características Principales

### Roles de Usuario
El sistema cuenta con 4 roles diferentes, cada uno con permisos específicos:

1. **Administrador**
   - Crear, editar y eliminar usuarios del sistema
   - Asignar roles y credenciales (RUT y contraseña)
   - Acceso completo a todas las funcionalidades
   - Vista general de estadísticas del sistema

2. **Recepcionista**
   - Gestión completa de pacientes (crear, editar, ver, eliminar)
   - Agendar, modificar y cancelar citas médicas
   - Consultar información de pacientes y citas

3. **Médico**
   - Ver lista de pacientes y sus historias clínicas
   - Gestionar sus propias citas médicas
   - Actualizar diagnósticos y tratamientos
   - Emitir recetas médicas
   - Editar historias clínicas

4. **Enfermera**
   - Registrar signos vitales de pacientes
   - Ver citas programadas
   - Crear y actualizar historias clínicas
   - Consultar información de pacientes

### Funcionalidades por Módulo

#### 👤 Gestión de Usuarios (Solo Administrador)
- Crear usuarios con RUT chileno como identificador único
- Asignar roles y permisos
- Gestionar credenciales de acceso
- Campos específicos para médicos (especialidad, número de registro)

#### 🏥 Gestión de Pacientes
- Registro completo de datos personales
- RUT como identificador único
- Datos de contacto y emergencia
- Información médica básica
- Búsqueda rápida por nombre o RUT

#### 📋 Historia Clínica
- Grupo sanguíneo
- Alergias conocidas
- Enfermedades crónicas
- Medicamentos actuales
- Observaciones médicas
- Registro de quién actualiza la información

#### 📅 Gestión de Citas Médicas
- Agendar citas con médicos específicos
- Estados: Pendiente, Confirmada, En Curso, Completada, Cancelada
- Registro de diagnóstico y tratamiento
- Filtros por fecha y estado
- Vista de agenda del día

#### 💊 Recetas Médicas (Solo Médicos)
- Emisión de recetas asociadas a citas
- Detalle de medicamentos, dosis y frecuencia
- Indicaciones para el paciente
- Fecha de vigencia
- Función de impresión

#### 🩺 Signos Vitales (Enfermeras)
- Presión arterial
- Frecuencia cardíaca
- Temperatura corporal
- Frecuencia respiratoria
- Saturación de oxígeno
- Peso y altura (opcional)
- Asociación opcional con citas

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/NicoG56/GestionClinica.git
cd GestionClinica
```

### Paso 2: Crear Entorno Virtual
```bash
python -m venv .venv
```

#### Activar el entorno virtual:
- Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- Windows (CMD):
  ```cmd
  .venv\Scripts\activate.bat
  ```
- Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```

### Paso 3: Instalar Dependencias
```bash
pip install django mysqlclient
```

### Paso 4: Configurar Base de Datos

1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE gestion_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configurar credenciales en `gestion_clinica/settings.py`:
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

### Paso 5: Aplicar Migraciones
```bash
python manage.py migrate
```

### Paso 6: Crear Superusuario
```bash
python crear_superusuario.py
```

Este script creará un usuario administrador con las siguientes credenciales:
- **RUT:** 11111111-1
- **Contraseña:** admin123
- **Rol:** Administrador

**⚠️ IMPORTANTE:** Cambie la contraseña después del primer inicio de sesión.

### Paso 7: Iniciar el Servidor
```bash
python manage.py runserver
```

Acceder al sistema en: http://127.0.0.1:8000/

## 📱 Uso del Sistema

### Primer Acceso
1. Acceder a http://127.0.0.1:8000/
2. Iniciar sesión con las credenciales del administrador
3. Crear usuarios para médicos, enfermeras y recepcionistas
4. Cada usuario usará su RUT como nombre de usuario

### Formato de RUT
El RUT debe ingresarse en formato: `12345678-9`
- 7-8 dígitos
- Guión
- Dígito verificador (puede ser K)

### Flujo de Trabajo Típico

1. **Administrador** crea usuarios del sistema
2. **Recepcionista** registra nuevos pacientes
3. **Recepcionista** agenda citas médicas
4. **Enfermera** registra signos vitales antes de la consulta
5. **Médico** atiende la cita y actualiza diagnóstico
6. **Médico** emite receta médica si es necesario

## 🗂️ Estructura del Proyecto

```
gestionClinica/
├── gestion_clinica/          # Configuración del proyecto
│   ├── settings.py          # Configuración general
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # WSGI config
├── gestor_app/              # Aplicación principal
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Lógica de vistas
│   ├── forms.py             # Formularios
│   ├── urls.py              # URLs de la app
│   ├── admin.py             # Admin de Django
│   ├── templates/           # Templates HTML
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard_*.html
│   │   ├── usuarios/
│   │   ├── pacientes/
│   │   ├── citas/
│   │   ├── recetas/
│   │   ├── signos/
│   │   └── historia/
│   ├── static/              # Archivos estáticos
│   │   ├── estilos/
│   │   └── img/
│   └── migrations/          # Migraciones de BD
├── manage.py                # Comando Django
├── crear_superusuario.py   # Script inicial
└── README.md               # Este archivo
```

## 🔒 Seguridad

- Autenticación requerida para todas las vistas (excepto login)
- Control de acceso basado en roles
- Validación de RUT chileno
- Passwords hasheados con PBKDF2
- Protección CSRF en formularios
- Sesiones seguras

## 🎨 Tecnologías Utilizadas

- **Backend:** Django 5.2.8
- **Base de Datos:** MySQL
- **Frontend:** Bootstrap 5.3
- **Iconos:** Bootstrap Icons
- **Autenticación:** Django Authentication System con modelo personalizado

## 📊 Modelos de Datos

### CustomUser
Usuario personalizado con RUT como identificador único y soporte para roles.

### Paciente
Información completa del paciente incluyendo datos personales y de contacto.

### HistoriaClinica
Historia médica del paciente con información relevante.

### Cita
Citas médicas con estados y seguimiento completo.

### RecetaMedica
Recetas emitidas por médicos con medicamentos e indicaciones.

### SignosVitales
Registro de signos vitales tomados por enfermeras.

## 🔧 Panel de Administración Django

Acceder a: http://127.0.0.1:8000/admin/

El panel de administración de Django está disponible para el superusuario y permite:
- Gestión directa de todos los modelos
- Búsqueda y filtrado avanzado
- Exportación de datos
- Registro de cambios (log de acciones)

## 📝 Notas Adicionales

### Validaciones
- RUT válido (formato y dígito verificador)
- Fechas coherentes
- Campos obligatorios según rol
- Especialidad obligatoria para médicos

### Características Adicionales
- Búsqueda rápida de pacientes
- Filtros en listados
- Dashboards personalizados por rol
- Estadísticas en tiempo real
- Interfaz responsive (móvil/tablet/desktop)

## 🐛 Resolución de Problemas

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
```

### Error de conexión a MySQL
Verificar que MySQL esté ejecutándose y las credenciales sean correctas.

### Error: "Table doesn't exist"
```bash
python manage.py migrate
```

## 👥 Credenciales de Prueba

### Superusuario Administrador
- **RUT:** 11111111-1
- **Contraseña:** admin123

Puede crear usuarios de prueba con diferentes roles desde el panel de administrador.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 👨‍💻 Autor

Desarrollado como sistema de gestión clínica completo con Django.

---

**Nota:** Este es un sistema de desarrollo. Para uso en producción, implemente medidas de seguridad adicionales:
- Configurar SECRET_KEY segura
- Establecer DEBUG = False
- Configurar ALLOWED_HOSTS
- Usar HTTPS
- Implementar respaldos de base de datos
- Configurar logs de auditoría
- Implementar rate limiting
