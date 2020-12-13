from string import digits, punctuation

from django.contrib.auth.models import User
from django.test import TestCase

from booking.forms import AppointmentForm
from booking.models import Appointment, Doctor
from .common import *


class BookingTest(TestCase):
    """Проверка записи на приём"""

    form = user = doctor = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.doctor = Doctor.objects.create(user=cls.user, specialty=SPECIALTY)

    def test_create_appointment_positive(self):
        """Проверка возможности записи на приём"""
        date, time = get_next_date_time()
        form_data = {
            'visitor': random_str(),
            'doctor': self.doctor.id,
            'date': date,
            'time': time,
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_appointment_exists(self):
        """Проверка валидации при записи на уже зарезервированное время"""
        date, time = get_next_date_time()
        visitor = random_str()

        Appointment.objects.create(
            doctor=self.doctor,
            visitor=visitor,
            date=date,
            time=time,
        )
        form_data = {
            'visitor': visitor,
            'doctor': self.doctor.id,
            'date': date.strftime('%d.%m.%Y'),
            'time': time,
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())

        errors = form.errors.get('__all__', [])
        self.assertTrue(errors)
        for error in errors:
            self.assertIn('уже существует', error)

    def test_bad_name(self):
        """Проверка валидации имени"""
        date, time = get_next_date_time('%d.%m.%Y')
        form_data = {
            'doctor': self.doctor.id,
            'date': date,
            'time': time,
        }

        test_data = [
            ('ab', 'to short'),
            ('c' * 256, 'too long'),
            (digits, 'digits'),
            (punctuation, 'punctuation'),
        ]

        for case, name in test_data:
            with self.subTest(name):
                form_data['visitor'] = case
                form = AppointmentForm(data=form_data)
                self.assertFalse(form.is_valid())

                errors = form.errors.get('visitor', [])
                self.assertTrue(errors)
