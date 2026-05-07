from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
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
# LIST — Listado de reservas
# ---------------------------------------------------------------------------
class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        # Staff ve todas; usuarios normales solo las suyas
        if self.request.user.is_staff:
            return Reserva.objects.select_related("usuario").all()
        return Reserva.objects.filter(usuario=self.request.user)


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
