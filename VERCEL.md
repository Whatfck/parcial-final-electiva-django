# Instrucciones para Vercel

## ⚠️ CONFIGURACIÓN REQUERIDA EN EL DASHBOARD

El archivo `vercel.json` está configured para usar los Build Settings del dashboard. **DEBES configurar manualmente en Vercel:**

### 1. Conectar Repositorio
- Conecta `github.com/Whatfck/parcial-final-electiva-django` 
- Selecciona rama `Dev1`

### 2. Framework y Build Settings (IMPORTANTE)

Ve a tu proyecto en Vercel → **Settings** → **Build & Development Settings**:

**Framework Preset**: Django

**Build Command**:
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Output Directory**: Dejar en blanco (blank)

**Install Command**: 
```
pip install -r requirements.txt
```

### 3. Variables de Entorno

En **Settings** → **Environment Variables**, añade:

| Variable | Valor | Notas |
|----------|-------|-------|
| `SECRET_KEY` | Tu clave secreta | Usa un valor seguro y aleatorio |
| `DEBUG` | `False` | IMPORTANTE: False en producción |
| `ALLOWED_HOSTS` | `.vercel.app` | Permite todos los subdominios de Vercel |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` | Para protección CSRF |

### 4. Redeploy

Una vez guardada la configuración, haz un **Redeploy** o un nuevo push a `Dev1`.

## Dominio

Una vez desplegado correctamente, la aplicación estará en:
```
https://parcial-final-electiva-django-git-dev1-[usuario]-[equipo].vercel.app
```

## Verificación

- ✅ CSS debe cargar (no error de MIME type)
- ✅ Plantillas HTML deben renderizar
- ✅ Sistema de login debe funcionar
- ✅ Redireccionamientos funcionar correctamente

## Troubleshooting

### Error: CSS no se carga (MIME type text/html)
👉 Verifica que **Build Command** incluya `collectstatic --noinput`

### Error: No module named 'django'
👉 Verifica que **Install Command** sea `pip install -r requirements.txt`

### Error: Database error
👉 Las migraciones se ejecutan automáticamente en el **Build Command**

### Error: 404 en todas las rutas
👉 Verifica que **DEBUG=False** esté configurado en variables de entorno

