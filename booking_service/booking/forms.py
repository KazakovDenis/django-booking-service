from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Appointment


_CURRENT_YEAR = date.today().year
_YEARS = range(_CURRENT_YEAR, _CURRENT_YEAR + 2)


class AppointmentForm(forms.ModelForm):
    """Форма записи на приём"""
    visitor = forms.CharField(label=_('Ваши имя и фамилия'), max_length=255)
    date = forms.DateField(widget=forms.SelectDateWidget(years=_YEARS))

    class Meta:
        model = Appointment
        fields = '__all__'
