from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Форма записи на приём"""
    class Meta:
        model = Appointment
        fields = '__all__'
