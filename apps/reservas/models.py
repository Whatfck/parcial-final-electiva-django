from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "Pendiente", "Pendiente"
        APROBADA = "Aprobada", "Aprobada"
        RECHAZADA = "Rechazada", "Rechazada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas",
    )
    laboratorio = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    motivo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "hora_inicio"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        indexes = [
            models.Index(fields=["fecha", "laboratorio"], name="idx_reserva_fecha_lab"),
            models.Index(fields=["estado"], name="idx_reserva_estado"),
        ]

    def clean(self):
        super().clean()
        if self.hora_inicio and self.hora_fin and self.hora_inicio >= self.hora_fin:
            raise ValidationError({
                "hora_fin": "La hora de fin debe ser mayor que la hora de inicio."
            })

    def __str__(self):
        return f"{self.laboratorio} - {self.fecha}"
