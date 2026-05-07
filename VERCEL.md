# Instrucciones para Vercel

## Configuración Requerida

Para que el proyecto funcione correctamente en Vercel, sigue estos pasos:

### 1. Conectar el Repositorio
- Conecta tu repositorio de GitHub a Vercel
- Selecciona la rama `Dev1` como la rama a desplegar

### 2. Configurar Build Command (IMPORTANTE)

En el dashboard de Vercel:
1. Ve a tu proyecto
2. Entra en **Settings** → **Build & Development Settings**
3. En **Build Command**, ingresa:
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```
4. En **Output Directory**, dejar vacío (por defecto)

### 3. Configurar Variables de Entorno

En el dashboard de Vercel, agrega estas variables de entorno:

```
SECRET_KEY=tu-clave-secreta-segura-aqui
DEBUG=False
ALLOWED_HOSTS=.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
```

### 4. Guardar y Desplegar

- Guarda los cambios
- Vercel desplegará automáticamente
- En el primer despliegue tardará más tiempo (ejecutando collectstatic)

## Notas Importantes

- **Base de datos**: Actualmente usa SQLite. Para producción con múltiples instancias, considera usar PostgreSQL
- **Archivos estáticos**: Se servirán con WhiteNoise directamente desde Django
- **Migraciones**: Se ejecutan automáticamente en cada despliegue

## Solución de Problemas

### Error: CSS no se carga (MIME type text/html)
Este error indica que `collectstatic` no se ejecutó correctamente. Verifica que el **Build Command** esté configurado correctamente en Vercel.

### Error: Base de datos no existe
Asegúrate que el **Build Command** incluya `python manage.py migrate`

### Error: 404 en rutas
Verifica que `DEBUG=False` esté configurado y que la variable `ALLOWED_HOSTS` incluya tu dominio de Vercel

## Dominio Vercel

Una vez desplegado, tu aplicación estará disponible en:
```
https://[proyecto-id]-[equipo].vercel.app
```

Por ejemplo:
```
https://parcial-final-electiva-django-git-dev1-whatfcks-projects.vercel.app
```
