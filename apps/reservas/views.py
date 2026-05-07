from csv import writer as csv_writer
from datetime import timedelta
from io import StringIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from apps.reservas.forms import ReservaForm
from apps.reservas.models import Reserva


# ---------------------------------------------------------------------------
# Mixin de utilidad: solo el dueño o un admin puede actuar sobre la reserva
# ---------------------------------------------------------------------------
class ReservaOwnerMixin:
    """Garantiza que únicamente el propietario o un staff pueda acceder."""

    def get_object(self, queryset=None):
        reserva = super().get_object(queryset)
        if not (self.request.user.is_staff or reserva.usuario == self.request.user):
            raise PermissionDenied
        return reserva


# ---------------------------------------------------------------------------
# Mixin: la reserva debe estar en estado Pendiente para editar/eliminar
# ---------------------------------------------------------------------------
class SoloPendienteMixin(ReservaOwnerMixin):
    """Bloquea la acción si la reserva ya fue aprobada o rechazada."""

    def get_object(self, queryset=None):
        reserva = super().get_object(queryset)
        if reserva.estado != Reserva.Estado.PENDIENTE:
            messages.error(
                self.request,
                "Solo se pueden modificar reservas en estado Pendiente.",
            )
            raise PermissionDenied
        return reserva


# ---------------------------------------------------------------------------
# Función auxiliar: detecta conflictos de horario en el mismo laboratorio
# ---------------------------------------------------------------------------
def hay_conflicto(laboratorio, fecha, hora_inicio, hora_fin, excluir_id=None):
    """
    Retorna True si ya existe una reserva (no rechazada) en el mismo
    laboratorio y fecha que se superpone con el rango [hora_inicio, hora_fin).
    """
    qs = Reserva.objects.filter(
        laboratorio=laboratorio,
        fecha=fecha,
    ).exclude(estado=Reserva.Estado.RECHAZADA)

    if excluir_id:
        qs = qs.exclude(pk=excluir_id)

    # Superposición: el inicio propuesto < fin existente  Y  el fin propuesto > inicio existente
    qs = qs.filter(
        Q(hora_inicio__lt=hora_fin) & Q(hora_fin__gt=hora_inicio)
    )
    return qs.exists()


# ---------------------------------------------------------------------------
# LIST — Listado de reservas con filtros
# ---------------------------------------------------------------------------
class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        # Staff ve todas; usuarios normales solo las suyas
        if self.request.user.is_staff:
            qs = Reserva.objects.select_related("usuario").all()
        else:
            qs = Reserva.objects.filter(usuario=self.request.user)

        # Filtro por fecha
        fecha = self.request.GET.get("fecha")
        if fecha:
            qs = qs.filter(fecha=fecha)

        # Filtro por laboratorio
        laboratorio = self.request.GET.get("laboratorio")
        if laboratorio:
            qs = qs.filter(laboratorio__icontains=laboratorio)

        # Filtro por estado (solo si es admin)
        if self.request.user.is_staff:
            estado = self.request.GET.get("estado")
            if estado and estado != "todos":
                qs = qs.filter(estado=estado)

        return qs.order_by("-fecha", "hora_inicio")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["fecha_filtro"] = self.request.GET.get("fecha", "")
        ctx["laboratorio_filtro"] = self.request.GET.get("laboratorio", "")
        ctx["estado_filtro"] = self.request.GET.get("estado", "todos")
        ctx["estados"] = Reserva.Estado.choices
        return ctx


# ---------------------------------------------------------------------------
# DETAIL — Detalle de una reserva
# ---------------------------------------------------------------------------
class ReservaDetailView(LoginRequiredMixin, ReservaOwnerMixin, DetailView):
    model = Reserva
    template_name = "reservas/reserva_detail.html"
    context_object_name = "reserva"


# ---------------------------------------------------------------------------
# CREATE — Nueva reserva
# ---------------------------------------------------------------------------
class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    success_url = reverse_lazy("reservas:lista")

    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.usuario = self.request.user

        if hay_conflicto(
            reserva.laboratorio,
            reserva.fecha,
            reserva.hora_inicio,
            reserva.hora_fin,
        ):
            form.add_error(
                None,
                "Ya existe una reserva en ese laboratorio que se superpone con el horario indicado.",
            )
            return self.form_invalid(form)

        reserva.save()
        messages.success(self.request, "Reserva creada correctamente.")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Nueva reserva"
        ctx["accion"] = "Crear"
        return ctx


# ---------------------------------------------------------------------------
# UPDATE — Editar reserva (solo si está Pendiente y el usuario es el dueño/staff)
# ---------------------------------------------------------------------------
class ReservaUpdateView(LoginRequiredMixin, SoloPendienteMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    success_url = reverse_lazy("reservas:lista")

    def form_valid(self, form):
        reserva = form.save(commit=False)

        if hay_conflicto(
            reserva.laboratorio,
            reserva.fecha,
            reserva.hora_inicio,
            reserva.hora_fin,
            excluir_id=reserva.pk,
        ):
            form.add_error(
                None,
                "Ya existe una reserva en ese laboratorio que se superpone con el horario indicado.",
            )
            return self.form_invalid(form)

        reserva.save()
        messages.success(self.request, "Reserva actualizada correctamente.")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar reserva"
        ctx["accion"] = "Guardar cambios"
        return ctx


# ---------------------------------------------------------------------------
# DELETE — Eliminar reserva (solo si está Pendiente y el usuario es el dueño/staff)
# ---------------------------------------------------------------------------
class ReservaDeleteView(LoginRequiredMixin, SoloPendienteMixin, DeleteView):
    model = Reserva
    template_name = "reservas/reserva_confirm_delete.html"
    context_object_name = "reserva"
    success_url = reverse_lazy("reservas:lista")

    def form_valid(self, form):
        messages.success(self.request, "Reserva eliminada correctamente.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# APPROVE — Aprobar reserva (solo admin)
# ---------------------------------------------------------------------------
class ReservaApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.estado != Reserva.Estado.PENDIENTE:
            messages.error(request, "Solo se pueden aprobar reservas en estado Pendiente.")
            return redirect("reservas:lista")

        reserva.estado = Reserva.Estado.APROBADA
        reserva.save()
        messages.success(request, f"Reserva aprobada: {reserva.laboratorio} el {reserva.fecha}")
        return redirect("reservas:detalle", pk=pk)


# ---------------------------------------------------------------------------
# REJECT — Rechazar reserva (solo admin)
# ---------------------------------------------------------------------------
class ReservaRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.estado != Reserva.Estado.PENDIENTE:
            messages.error(request, "Solo se pueden rechazar reservas en estado Pendiente.")
            return redirect("reservas:lista")

        reserva.estado = Reserva.Estado.RECHAZADA
        reserva.save()
        messages.success(request, f"Reserva rechazada: {reserva.laboratorio} el {reserva.fecha}")
        return redirect("reservas:detalle", pk=pk)


# ---------------------------------------------------------------------------
# STATS — Estadísticas de uso de laboratorios (solo admin)
# ---------------------------------------------------------------------------
class ReservaStatsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "reservas/reserva_stats.html"
    
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # Total de reservas
        ctx["total_reservas"] = Reserva.objects.count()
        ctx["total_aprobadas"] = Reserva.objects.filter(estado=Reserva.Estado.APROBADA).count()
        ctx["total_pendientes"] = Reserva.objects.filter(estado=Reserva.Estado.PENDIENTE).count()
        ctx["total_rechazadas"] = Reserva.objects.filter(estado=Reserva.Estado.RECHAZADA).count()
        
        # Laboratorios más usados
        ctx["labs_mas_usados"] = (
            Reserva.objects
            .filter(estado=Reserva.Estado.APROBADA)
            .values("laboratorio")
            .annotate(cantidad=Count("id"))
            .order_by("-cantidad")[:5]
        )
        
        # Docentes más activos
        ctx["docentes_activos"] = (
            Reserva.objects
            .filter(estado=Reserva.Estado.APROBADA)
            .values("usuario__username")
            .annotate(cantidad=Count("id"))
            .order_by("-cantidad")[:5]
        )
        
        # Uso en los últimos 7 días
        fecha_hace_7_dias = timezone.now().date() - timedelta(days=7)
        ctx["reservas_ultimos_7_dias"] = Reserva.objects.filter(
            fecha__gte=fecha_hace_7_dias,
            estado=Reserva.Estado.APROBADA
        ).count()
        
        return ctx


# ---------------------------------------------------------------------------
# EXPORT CSV — Descargar reservas en CSV (solo admin)
# ---------------------------------------------------------------------------
class ReservaExportCSVView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        # Obtener parámetros de filtrado
        fecha = request.GET.get("fecha")
        laboratorio = request.GET.get("laboratorio")
        
        qs = Reserva.objects.select_related("usuario")
        
        if fecha:
            qs = qs.filter(fecha=fecha)
        if laboratorio:
            qs = qs.filter(laboratorio__icontains=laboratorio)
        
        # Crear CSV en memoria
        output = StringIO()
        writer = csv_writer(output)
        
        # Encabezados
        writer.writerow([
            "ID", "Usuario", "Laboratorio", "Fecha", 
            "Hora Inicio", "Hora Fin", "Estado", "Motivo", "Fecha Creación"
        ])
        
        # Filas de datos
        for reserva in qs:
            writer.writerow([
                reserva.id,
                reserva.usuario.username,
                reserva.laboratorio,
                reserva.fecha.strftime("%d/%m/%Y"),
                reserva.hora_inicio.strftime("%H:%M"),
                reserva.hora_fin.strftime("%H:%M"),
                reserva.estado,
                reserva.motivo[:50],  # Primeros 50 caracteres
                reserva.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
            ])
        
        # Preparar respuesta
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=reservas.csv"
        return response
