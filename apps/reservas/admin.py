from django.contrib import admin

from apps.reservas.models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("laboratorio", "usuario", "fecha", "hora_inicio", "hora_fin", "estado")
    list_filter = ("estado", "fecha", "laboratorio")
    search_fields = ("laboratorio", "motivo", "usuario__username")
    ordering = ("-fecha", "hora_inicio")
    date_hierarchy = "fecha"
    readonly_fields = ("fecha_creacion",)
