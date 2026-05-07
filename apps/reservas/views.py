from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView

import csv
from datetime import datetime

from apps.reservas.forms import ReservaForm
from apps.reservas.models import Reserva


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/lista.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros
        laboratorio = self.request.GET.get("laboratorio")
        fecha = self.request.GET.get("fecha")
        estado = self.request.GET.get("estado")

        if laboratorio:
            queryset = queryset.filter(laboratorio__icontains=laboratorio)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        if estado:
            queryset = queryset.filter(estado=estado)

        # Si no es admin, solo ver sus propias reservas
        if not self.request.user.is_staff:
            queryset = queryset.filter(usuario=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["laboratorios"] = Reserva.objects.values_list("laboratorio", flat=True).distinct()
        return context


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/form.html"
    success_url = reverse_lazy("reservas:lista")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        # Validar conflictos de horario
        conflictos = Reserva.objects.filter(
            laboratorio=form.instance.laboratorio,
            fecha=form.instance.fecha,
            estado__in=["Pendiente", "Aprobada"],
        ).filter(
            Q(hora_inicio__lt=form.instance.hora_fin, hora_fin__gt=form.instance.hora_inicio)
        ).exclude(pk=form.instance.pk)
        if conflictos.exists():
            form.add_error(None, "Ya existe una reserva en ese horario para este laboratorio.")
            return self.form_invalid(form)
        messages.success(self.request, "Reserva creada exitosamente.")
        return super().form_valid(form)


class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/form.html"
    success_url = reverse_lazy("reservas:lista")

    def test_func(self):
        reserva = self.get_object()
        return reserva.usuario == self.request.user and reserva.estado == "Pendiente"

    def form_valid(self, form):
        # Validar conflictos
        conflictos = Reserva.objects.filter(
            laboratorio=form.instance.laboratorio,
            fecha=form.instance.fecha,
            estado__in=["Pendiente", "Aprobada"],
        ).filter(
            Q(hora_inicio__lt=form.instance.hora_fin, hora_fin__gt=form.instance.hora_inicio)
        ).exclude(pk=form.instance.pk)
        if conflictos.exists():
            form.add_error(None, "Ya existe una reserva en ese horario para este laboratorio.")
            return self.form_invalid(form)
        messages.success(self.request, "Reserva actualizada exitosamente.")
        return super().form_valid(form)


class ReservaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reserva
    template_name = "reservas/confirm_delete.html"
    success_url = reverse_lazy("reservas:lista")

    def test_func(self):
        reserva = self.get_object()
        return reserva.usuario == self.request.user and reserva.estado == "Pendiente"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Reserva eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)


class ReservaAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reserva
    template_name = "reservas/lista_admin.html"
    context_object_name = "reservas"
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        laboratorio = self.request.GET.get("laboratorio")
        fecha = self.request.GET.get("fecha")
        estado = self.request.GET.get("estado")

        if laboratorio:
            queryset = queryset.filter(laboratorio__icontains=laboratorio)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["laboratorios"] = Reserva.objects.values_list("laboratorio", flat=True).distinct()
        return context


def aprobar_reserva(request, pk):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para esta acción.")
        return redirect("reservas:lista_admin")
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.estado == "Pendiente":
        reserva.estado = "Aprobada"
        reserva.save()
        messages.success(request, "Reserva aprobada.")
    else:
        messages.error(request, "Solo se pueden aprobar reservas pendientes.")
    return redirect("reservas:lista_admin")


def rechazar_reserva(request, pk):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para esta acción.")
        return redirect("reservas:lista_admin")
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.estado == "Pendiente":
        reserva.estado = "Rechazada"
        reserva.save()
        messages.success(request, "Reserva rechazada.")
    else:
        messages.error(request, "Solo se pueden rechazar reservas pendientes.")
    return redirect("reservas:lista_admin")


class EstadisticasView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "reservas/estadisticas.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estadísticas
        total_reservas = Reserva.objects.count()
        reservas_aprobadas = Reserva.objects.filter(estado="Aprobada").count()
        reservas_pendientes = Reserva.objects.filter(estado="Pendiente").count()
        reservas_rechazadas = Reserva.objects.filter(estado="Rechazada").count()

        # Por laboratorio
        por_laboratorio = Reserva.objects.values("laboratorio").annotate(
            total=Count("id"),
            aprobadas=Count("id", filter=Q(estado="Aprobada")),
            pendientes=Count("id", filter=Q(estado="Pendiente")),
            rechazadas=Count("id", filter=Q(estado="Rechazada")),
        ).order_by("-total")

        context.update({
            "total_reservas": total_reservas,
            "reservas_aprobadas": reservas_aprobadas,
            "reservas_pendientes": reservas_pendientes,
            "reservas_rechazadas": reservas_rechazadas,
            "por_laboratorio": por_laboratorio,
        })
        return context


def exportar_csv(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para esta acción.")
        return redirect("reservas:lista_admin")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="reservas_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Usuario", "Laboratorio", "Fecha", "Hora Inicio", "Hora Fin", "Estado", "Motivo", "Fecha Creación"])

    reservas = Reserva.objects.all().select_related("usuario")
    for reserva in reservas:
        writer.writerow([
            reserva.usuario.username,
            reserva.laboratorio,
            reserva.fecha,
            reserva.hora_inicio,
            reserva.hora_fin,
            reserva.estado,
            reserva.motivo,
            reserva.fecha_creacion,
        ])

    return response