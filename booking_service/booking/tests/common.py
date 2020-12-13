from datetime import date as _date, timedelta as _td
from random import sample as _sample
from string import ascii_letters as _letters

from django.urls import reverse


USERNAME = 'test_user'
PASSWORD = 'sup3rs3cr3tp@$$'
EMAIL = 'test@email.com'
CREDENTIALS = {'username': USERNAME, 'password': PASSWORD}
SPECIALTY = 'therapist'

TODAY = _date.today()
START_TIME, END_TIME = 9, 17
used_date = TODAY
used_time = START_TIME


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
    """Получить случайную строку указанной длины"""
    return ''.join(_sample(_letters, length))


def get_next_date_time(fmt: str = ''):
    """Получить следующие валидные дату и время"""
    global used_date, used_time

    if used_date.isoweekday() > 5:
        used_date += _td(days=2)

    date, time = used_date, used_time
    if used_time == END_TIME:
        used_date += _td(days=1)
        used_time = START_TIME
    else:
        used_time += 1

    if fmt:
        date = date.strftime(fmt)

    return date, time
