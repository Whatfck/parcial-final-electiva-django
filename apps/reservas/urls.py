from django.urls import path

from apps.reservas import views

app_name = "reservas"

urlpatterns = [
    # Listado y CRUD
    path("", views.ReservaListView.as_view(), name="lista"),
    path("nueva/", views.ReservaCreateView.as_view(), name="crear"),
    path("<int:pk>/", views.ReservaDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.ReservaUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.ReservaDeleteView.as_view(), name="eliminar"),
    
    # Admin: Aprobación y rechazo
    path("<int:pk>/aprobar/", views.ReservaApproveView.as_view(), name="aprobar"),
    path("<int:pk>/rechazar/", views.ReservaRejectView.as_view(), name="rechazar"),
    
    # Admin: Estadísticas y exportación
    path("estadisticas/", views.ReservaStatsView.as_view(), name="estadisticas"),
    path("exportar-csv/", views.ReservaExportCSVView.as_view(), name="exportar_csv"),
]
