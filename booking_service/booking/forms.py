from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext_lazy as _

from .models import Appointment
from .validators import date_validator, name_validator


class AppointmentForm(forms.ModelForm):
    """Форма записи на приём"""
    visitor = forms.CharField(
        label=_('Ваши имя и фамилия'),
        validators=[name_validator],
        error_messages={
            'bad_fio': _('Имя и фамилия указаны некорректно'),
            'max_length': _('Имя и фамилия слишком длинные'),
        }
    )
    date = forms.DateField(
        label=_('Дата приёма'),
        widget=AdminDateWidget,
        validators=[date_validator],
        error_messages={
            'bad_date': _(
                'Дата записи не может быть раньше сегодня, выходным днём, '
                'а также позднее 31 декабря следующего года'
            )
        }
    )

    class Meta:
        model = Appointment
        fields = ('visitor', 'doctor', 'date', 'time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrap_cls = {'class': 'form-control'}
        for field in ('visitor', 'doctor', 'time'):
            self.fields[field].widget.attrs.update(bootstrap_cls)
