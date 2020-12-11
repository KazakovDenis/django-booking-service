from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext_lazy as _

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Форма записи на приём"""
    class Meta:
        model = Appointment
        fields = ('visitor', 'doctor', 'date', 'time')
        labels = {
            'visitor': _('Ваши имя и фамилия'),
            'date': _('Дата приёма'),
        }
        widgets = {
            'date': AdminDateWidget,
        }
        error_messages = {
            'visitor': {
                'min_length': _('Имя и фамилия слишком короткие'),
                'max_length': _('Имя и фамилия слишком длинные'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_cls = {'class': 'form-control'}
        for field in ('visitor', 'doctor', 'time'):
            self.fields[field].widget.attrs.update(bootstrap_cls)
