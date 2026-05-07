# DEBERES DEL PROYECTO

## Base común para todo el equipo

Para mantener consistencia en el desarrollo, todo el proyecto debe seguir estas reglas:

- Usar una estructura modular por aplicaciones.
- Mantener una sola plantilla base para encabezado, navegación y estilos generales.
- Trabajar con vistas basadas en clases cuando aplique.
- Validar permisos en la vista y no solo en la interfaz.
- Reutilizar la misma nomenclatura en modelos, urls, plantillas, formularios y mensajes.
- Documentar cualquier decisión técnica que afecte a otro integrante.

## Reparto por dev

### Dev1

Responsable de dejar la base del proyecto lista para que los demás trabajen sobre una estructura estable.

- Crear y configurar el proyecto Django.
- Crear las aplicaciones base del sistema.
- Configurar autenticación, inicio de sesión y cierre de sesión.
- Definir el modelo principal de reservas con sus campos y estados.
- Crear las migraciones iniciales.
- Preparar la plantilla base y la navegación principal.
- Dejar una estructura de carpetas clara y repetible.

### Dev2

Responsable de la lógica operativa de las reservas.

- Implementar el CRUD de reservas.
- Validar que no existan conflictos de horario en el mismo laboratorio.
- Permitir editar o eliminar solo reservas en estado Pendiente.
- Restringir acciones según el rol del usuario.
- Crear formularios y vistas manteniendo el mismo estilo del proyecto.
- Conectar las urls con las vistas correspondientes.

### Dev3

Responsable de la parte administrativa, reportes y cierre funcional.

- Aprobar o rechazar reservas desde el rol administrador.
- Crear listados con filtros por fecha y laboratorio.
- Implementar estadísticas de uso.
- Exportar reservas a CSV.
- Ajustar mensajes, vistas finales y detalles visuales.
- Revisar que la presentación final conserve la misma estructura definida por Dev1.

## Flujo recomendado de trabajo

1. Dev1 prepara la base técnica y funcional.
2. Dev2 construye el CRUD y las validaciones.
3. Dev3 agrega administración, reportes y exportación.
4. Antes de integrar cambios, revisar que todo siga la misma convención de nombres y estructura.

## Objetivo final

El proyecto debe quedar organizado, fácil de mantener y con responsabilidades claras para evitar duplicidad de trabajo o inconsistencias entre módulos.