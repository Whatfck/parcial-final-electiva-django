# Parcial final electiva Django

## EJERCICIO 1: Sistema de Gestión de Reservas de Laboratorios

**Objetivo general**

Desarrollar una aplicación Django que gestione las reservas de laboratorios, integrando autenticación, control de roles (docente y administrador) y validación de disponibilidad horaria **(nombre DEL PROYECTO_NOMBRE_ESTUDIANTE, nombre de las aplicaciones_ NOMBRE_ESTUDIANTE).**

**Requerimientos funcionales**

1. **Autenticación y roles**
    - Login y logout usando el sistema de usuarios de Django.
    - Roles:
        - Docente: crea, edita y cancela sus propias reservas.
        - Administrador: aprueba o rechaza cualquier reserva.

2. **Gestión de reservas (CRUD)**
    - Validar que no existan conflictos de horarios en el mismo laboratorio.
    - Permitir edición o eliminación solo si la reserva está en estado “Pendiente”.
    - El administrador puede cambiar el estado a “Aprobada” o “Rechazada”.

3. **Visualización y filtros**
    - Listar reservas filtradas por fecha o laboratorio.
    - Mostrar estadísticas de uso y exportación a CSV.
        **Requerimientos técnicos**
        - Uso de vistas basadas en clases (ListView, CreateView, UpdateView, DeleteView).
        - Control de acceso con LoginRequiredMixin y UserPassesTestMixin.
        - Diseño modular con plantillas base y estilos.

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