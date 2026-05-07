from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.reservas.models import Reserva
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Crea usuarios de prueba y reservas de ejemplo para demostración'

    def handle(self, *args, **options):
        # Admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin.set_password('Admin@123456')
        admin.save()
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Admin creado'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Admin actualizado'))

        # Docente 1
        user1, created = User.objects.get_or_create(
            username='carlos.mendez',
            defaults={
                'email': 'carlos.mendez@universidad.edu',
                'first_name': 'Carlos',
                'last_name': 'Méndez García',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user1.set_password('DocCarlos@2024')
        user1.save()
        status = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(f'✓ carlos.mendez {status}'))

        # Docente 2
        user2, created = User.objects.get_or_create(
            username='maria.lopez',
            defaults={
                'email': 'maria.lopez@universidad.edu',
                'first_name': 'María',
                'last_name': 'López Rodríguez',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user2.set_password('DocMaria@2024')
        user2.save()
        status = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(f'✓ maria.lopez {status}'))

        # Docente 3
        user3, created = User.objects.get_or_create(
            username='juan.torres',
            defaults={
                'email': 'juan.torres@universidad.edu',
                'first_name': 'Juan',
                'last_name': 'Torres Silva',
                'is_staff': False,
                'is_superuser': False
            }
        )
        user3.set_password('DocJuan@2024')
        user3.save()
        status = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(f'✓ juan.torres {status}'))

        # Crear reservas de ejemplo
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Reserva 1 - Aprobada
        reserva1, created = Reserva.objects.get_or_create(
            usuario=user1,
            laboratorio='Laboratorio de Redes',
            fecha=tomorrow,
            hora_inicio=time(9, 0),
            hora_fin=time(11, 0),
            defaults={
                'estado': 'Aprobada',
                'motivo': 'Clase de configuración de routers Cisco'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Reserva 1 creada: {reserva1.laboratorio} ({reserva1.estado})'
            ))

        # Reserva 2 - Pendiente
        reserva2, created = Reserva.objects.get_or_create(
            usuario=user2,
            laboratorio='Laboratorio de Sistemas',
            fecha=tomorrow,
            hora_inicio=time(14, 0),
            hora_fin=time(16, 0),
            defaults={
                'estado': 'Pendiente',
                'motivo': 'Práctica de administración de bases de datos'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Reserva 2 creada: {reserva2.laboratorio} ({reserva2.estado})'
            ))

        # Reserva 3 - Pendiente
        reserva3, created = Reserva.objects.get_or_create(
            usuario=user3,
            laboratorio='Laboratorio de Programación',
            fecha=(today + timedelta(days=2)),
            hora_inicio=time(10, 0),
            hora_fin=time(12, 0),
            defaults={
                'estado': 'Pendiente',
                'motivo': 'Desarrollo de aplicaciones en Python'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'✓ Reserva 3 creada: {reserva3.laboratorio} ({reserva3.estado})'
            ))

        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba listos!'))
