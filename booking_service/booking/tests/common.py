from datetime import date as _date
from random import sample as _sample
from string import ascii_letters as _letters

from django.urls import reverse


USERNAME = 'test_user'
PASSWORD = 'sup3rs3cr3tp@$$'
EMAIL = 'test@email.com'
CREDENTIALS = {'username': USERNAME, 'password': PASSWORD}
SPECIALTY = 'therapist'

TODAY = _date.today()
START_TIME = 9


class URL:
    ADMIN = reverse('admin:index')
    LOGIN = reverse('admin:login')
    LOGOUT = reverse('admin:logout')
    BOOKING = reverse('booking')
    SUCCESS = reverse('success')

    @staticmethod
    def schedule(doctor_id: int, **kwargs):
        if doctor_id:
            kwargs['id'] = doctor_id
        return reverse('schedule', kwargs=kwargs)


def random_str(length: int = 10) -> str:
    return ''.join(_sample(_letters, length))
