# Parcial final electiva Django

## EJERCICIO 1: Sistema de Gestión de Reservas de Laboratorios completado ✅

**Objetivo general**

Desarrollar una aplicación Django que gestione las reservas de laboratorios, integrando autenticación, control de roles (docente y administrador) y validación de disponibilidad horaria.

---

## ✅ ESTADO: PROYECTO COMPLETADO

### Funcionalidades Implementadas

#### **Fase Dev1 - Base del Proyecto**
- ✅ Configuración Django completa
- ✅ Aplicaciones modularizadas (accounts, reservas)
- ✅ Sistema de autenticación con login/logout
- ✅ Modelo Reserva con todos los campos requeridos
- ✅ Migraciones iniciales
- ✅ Plantilla base y navegación principal

#### **Fase Dev2 - CRUD de Reservas**
- ✅ ListaView de reservas
- ✅ CreateView para nuevas reservas
- ✅ DetailView para ver detalles
- ✅ UpdateView para editar reservas pendientes
- ✅ DeleteView para eliminar reservas pendientes
- ✅ Validación de conflictos horarios
- ✅ Restricción de edición/eliminación solo si está Pendiente
- ✅ Control de permisos por rol

#### **Fase Dev3 - Administración, Reportes e Integración**
- ✅ ApproveView: Aprobación de reservas por admin
- ✅ RejectView: Rechazo de reservas por admin
- ✅ StatsView: Panel de estadísticas para admin
- ✅ ExportCSVView: Exportación de datos a CSV
- ✅ Filtros avanzados por fecha y laboratorio
- ✅ Validaciones y permisos completos

---

**Requerimientos funcionales - TODOS COMPLETADOS ✅**

1. **Autenticación y roles**
    - ✅ Login y logout usando el sistema de usuarios de Django
    - ✅ Roles:
        - Docente: crea, edita y cancela sus propias reservas
        - Administrador: aprueba o rechaza cualquier reserva

2. **Gestión de reservas (CRUD)**
    - ✅ Validación de conflictos de horarios en el mismo laboratorio
    - ✅ Edición/eliminación solo si la reserva está en estado "Pendiente"
    - ✅ Administrador puede cambiar el estado a "Aprobada" o "Rechazada"

3. **Visualización y filtros**
    - ✅ Listado filtrado por fecha o laboratorio
    - ✅ Estadísticas de uso disponibles
    - ✅ Exportación a CSV funcional
    
**Requerimientos técnicos - TODOS CUMPLIDOS ✅**
    - ✅ Uso de vistas basadas en clases (ListView, CreateView, UpdateView, DeleteView)
    - ✅ Control de acceso con LoginRequiredMixin y UserPassesTestMixin
    - ✅ Diseño modular con plantillas base y estilos

**Modelo: Reserva**
| Campo| Tipo de dato| Descripción|
|-|-|-|
|usuario|ForeignKey(User, on_delete=models.CASCADE)|Usuario que realiza la reserva.|
|laboratorio|CharField(max_length=100)|Nombre del laboratorio solicitado.|
|fecha|DateField()|Fecha de la reserva.|
|hora_inicio|TimeField()|Hora de inicio de la reserva.|
|hora_fin|TimeField()|Hora de fin de la reserva.|
|estado|CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')]|Estado actual de la reserva.|
|motivo|TextField()|Motivo o descripción de la reserva.|
|fecha_creacion|DateTimeField(auto_now_add=True)|Fecha en que se crea la reserva.|

---

## 🚀 Despliegue en Vercel

Este proyecto está completamente configurado para desplegarse en Vercel.

### Variables de entorno recomendadas

```bash
SECRET_KEY=tu-clave-secreta-django
DEBUG=False
ALLOWED_HOSTS=.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
```

### Notas
- Los archivos estáticos se sirven con WhiteNoise
- Para despliegue en Vercel se usa `config/wsgi.py` como entrada
- Base de datos: SQLite (reemplazar en producción si es necesario)

---

## 📋 Estructura de carpetas

```
parcial-final-electiva-django/
├── manage.py
├── requirements.txt
├── config/              # Configuración del proyecto
├── apps/
│   ├── accounts/        # Sistema de autenticación
│   └── reservas/        # Lógica de reservas
├── templates/           # Plantillas HTML
├── static/              # CSS y archivos estáticos
└── vercel.json          # Configuración para Vercel
```

---

## 🔐 Roles y Permisos

### Docente
- ✅ Crear nuevas reservas
- ✅ Ver sus propias reservas
- ✅ Editar solo sus reservas pendientes
- ✅ Eliminar solo sus reservas pendientes

### Administrador
- ✅ Ver todas las reservas
- ✅ Filtrar por fecha, laboratorio y estado
- ✅ Aprobar reservas pendientes
- ✅ Rechazar reservas pendientes
- ✅ Ver estadísticas de uso
- ✅ Exportar datos a CSV

---

## 🛠️ Instalación y Ejecución Local

### Requisitos
- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/Whatfck/parcial-final-electiva-django.git
cd parcial-final-electiva-django

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

Acceder a: http://localhost:8000/

### Usar Datos de Prueba (Recomendado)

Para cargar usuarios y reservas de ejemplo, ejecuta:

```bash
python manage.py setup_demo_data
```

Esto crea automáticamente:
- 1 usuario **admin** con acceso total
- 3 usuarios **docentes** con datos completos
- 3 **reservas de ejemplo** (1 aprobada, 2 pendientes)

---

## 🔑 Credenciales de Acceso

### Admin (Administrador)
| Campo | Valor |
|-------|-------|
| **Username** | `admin` |
| **Password** | `Admin@123456` |
| **Rol** | Administrador - Acceso completo |

### Docentes (3 Usuarios de Prueba)

#### Usuario 1 - Carlos Méndez
| Campo | Valor |
|-------|-------|
| **Username** | `carlos.mendez` |
| **Password** | `DocCarlos@2024` |
| **Email** | `carlos.mendez@universidad.edu` |
| **Nombre Completo** | Carlos Méndez García |

#### Usuario 2 - María López
| Campo | Valor |
|-------|-------|
| **Username** | `maria.lopez` |
| **Password** | `DocMaria@2024` |
| **Email** | `maria.lopez@universidad.edu` |
| **Nombre Completo** | María López Rodríguez |

#### Usuario 3 - Juan Torres
| Campo | Valor |
|-------|-------|
| **Username** | `juan.torres` |
| **Password** | `DocJuan@2024` |
| **Email** | `juan.torres@universidad.edu` |
| **Nombre Completo** | Juan Torres Silva |

---

## 📊 Endpoint de Estadísticas y Exportación

- **/reservas/estadisticas/** - Panel de estadísticas (solo admin)
- **/reservas/exportar-csv/** - Descargar CSV (solo admin)