from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reserva",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("laboratorio", models.CharField(max_length=100)),
                ("fecha", models.DateField()),
                ("hora_inicio", models.TimeField()),
                ("hora_fin", models.TimeField()),
                ("estado", models.CharField(choices=[("Pendiente", "Pendiente"), ("Aprobada", "Aprobada"), ("Rechazada", "Rechazada")], default="Pendiente", max_length=20)),
                ("motivo", models.TextField()),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                (
                    "usuario",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reservas", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "verbose_name": "Reserva",
                "verbose_name_plural": "Reservas",
                "ordering": ["-fecha", "hora_inicio"],
                "indexes": [
                    models.Index(fields=["fecha", "laboratorio"]),
                    models.Index(fields=["estado"]),
                ],
            },
        ),
    ]
