from django.test import TestCase
from django.contrib.auth.models import User
from .models import Reserva

class ReservaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin = User.objects.create_superuser(username='admin', password='12345')
        self.reserva = Reserva.objects.create(
            usuario=self.user, laboratorio='Lab1', fecha='2023-01-01',
            hora_inicio='10:00', hora_fin='12:00', estado='pendiente'
        )

    def test_aprobar_reserva(self):
        self.client.login(username='admin', password='12345')
        response = self.client.post(f'/reservas/admin/aprobar/{self.reserva.pk}/', {'accion': 'aprobar'})
        self.reserva.refresh_from_db()
        self.assertEqual(self.reserva.estado, 'aprobada')

    def test_exportar_csv(self):
        self.client.login(username='admin', password='12345')
        response = self.client.get('/reservas/admin/exportar/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
