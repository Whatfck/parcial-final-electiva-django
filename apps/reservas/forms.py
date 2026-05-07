from django import forms

from apps.reservas.models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["laboratorio", "fecha", "hora_inicio", "hora_fin", "motivo"]
        labels = {
            "laboratorio": "Laboratorio",
            "fecha": "Fecha",
            "hora_inicio": "Hora de inicio",
            "hora_fin": "Hora de finalización",
            "motivo": "Motivo de la reserva",
        }
        widgets = {
            "laboratorio": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Lab 101, Laboratorio de Redes…",
            }),
            "fecha": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
            "hora_inicio": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control",
            }),
            "hora_fin": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control",
            }),
            "motivo": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe brevemente el propósito de la reserva…",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError(
                "La hora de finalización debe ser posterior a la hora de inicio."
            )
        return cleaned_data
