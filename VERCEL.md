# Instrucciones para Vercel

## ✨ Datos de Demostración

Los usuarios de prueba y reservas se crean **automáticamente** durante el build en Vercel.

### Credenciales Disponibles

**Administrador:**
- Username: `admin`
- Password: `Admin@123456`

**Docentes:**
1. `carlos.mendez` / `DocCarlos@2024`
2. `maria.lopez` / `DocMaria@2024`
3. `juan.torres` / `DocJuan@2024`

---

## ⚙️ Configuración Requerida en Vercel

El archivo `vercel.json` ya incluye el Build Command. **Solo necesitas:**

### 1. Variables de Entorno

En **Settings** → **Environment Variables**, añade:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | Clave aleatoria | Genera una clave segura |
| `DEBUG` | `False` | IMPORTANTE: False en producción |
| `ALLOWED_HOSTS` | `.vercel.app` | Permite subdominios de Vercel |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` | Protección CSRF |

### 2. Redeploy

- Guarda la configuración
- Haz un **Redeploy** o push a `Dev1`
- Los usuarios se crearán automáticamente durante el build

## 📋 Datos de Demostración

Se crean automáticamente:
- 1 usuario **admin** (Administrador)
- 3 usuarios **docentes** con nombres reales
- 3 **reservas de ejemplo** para probar funcionamiento:
  - 1 Aprobada
  - 2 Pendientes

## 🔄 Persistencia de Datos

⚠️ **Importante:**
- SQLite es local: los datos se pierden al redeploy
- Para producción con datos persistentes, usar **PostgreSQL** en lugar de SQLite
- Los usuarios se recreen automáticamente en cada build (idempotente)

## Troubleshooting

### Error: `setup_demo_data` command not found
- Verifica que `apps/reservas/management/commands/setup_demo_data.py` exista
- Asegúrate que los archivos `__init__.py` estén en los directorios

### Los usuarios no aparecen después del build
- Abre la consola de logs en Vercel
- Busca "Creando datos de demostración"
- Si hay errores, verifica que la estructura de directorios sea correcta

