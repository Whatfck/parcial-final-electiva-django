from django.urls import path

from apps.reservas.views import (
    ReservaListView,
    ReservaCreateView,
    ReservaUpdateView,
    ReservaDeleteView,
    ReservaAdminListView,
    aprobar_reserva,
    rechazar_reserva,
    EstadisticasView,
    exportar_csv,
)

app_name = "reservas"

urlpatterns = [
    path("", ReservaListView.as_view(), name="lista"),
    path("crear/", ReservaCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", ReservaUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", ReservaDeleteView.as_view(), name="eliminar"),
    path("admin/", ReservaAdminListView.as_view(), name="lista_admin"),
    path("<int:pk>/aprobar/", aprobar_reserva, name="aprobar"),
    path("<int:pk>/rechazar/", rechazar_reserva, name="rechazar"),
    path("estadisticas/", EstadisticasView.as_view(), name="estadisticas"),
    path("exportar-csv/", exportar_csv, name="exportar_csv"),
]
