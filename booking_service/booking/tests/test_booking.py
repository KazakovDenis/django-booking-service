from datetime import date, timedelta
from string import digits, punctuation

from django.contrib.auth.models import User
from django.test import TestCase

from booking.forms import AppointmentForm
from booking.models import Appointment, Doctor
from .common import *


def date_to_str(v):
    return v.strftime(FORM_DATE_FMT)


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
        visit_date, time = get_next_date_time()
        visitor = random_str()

        Appointment.objects.create(
            doctor=self.doctor,
            visitor=visitor,
            date=visit_date,
            time=time,
        )
        form_data = {
            'visitor': visitor,
            'doctor': self.doctor.id,
            'date': date_to_str(visit_date),
            'time': time,
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())

        errors = form.errors.get('__all__', [])
        self.assertTrue(errors)
        self.assertIn('уже существует', errors[0])

    def test_bad_name(self):
        """Проверка валидации имени"""
        visit_date, time = get_next_date_time('%d.%m.%Y')
        form_data = {
            'doctor': self.doctor.id,
            'date': visit_date,
            'time': time,
        }

        test_data = [
            ('Too short', 'ab'),
            ('Too long', 'c' * 256),
            ('Digits', digits),
            ('Punctuation', punctuation),
        ]

        for name, case in test_data:
            with self.subTest(name):
                form_data['visitor'] = case
                form = AppointmentForm(data=form_data)
                self.assertFalse(form.is_valid())

                errors = form.errors.get('visitor', [])
                self.assertTrue(errors)

    def test_bad_date(self):
        """Проверка валидации даты"""
        form_data = {
            'doctor': self.doctor.id,
            'visitor': random_str(),
            'time': START_TIME,
        }

        saturday = get_nearest_day_off()
        sunday = get_nearest_day_off() + timedelta(days=1)

        test_data = [
            ('In the past', date_to_str(date(2020, 12, 1))),
            ('Too far', date_to_str(date(2030, 12, 2))),
            ('Saturday', date_to_str(saturday)),
            ('Sunday', date_to_str(sunday)),
        ]

        for name, case in test_data:
            with self.subTest(name):
                form_data['date'] = case
                form = AppointmentForm(data=form_data)
                self.assertFalse(form.is_valid())

                errors = form.errors.get('date', [])
                self.assertTrue(errors)
