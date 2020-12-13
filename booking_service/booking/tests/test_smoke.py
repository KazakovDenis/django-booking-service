from django.contrib.auth.models import User
from django.test import TestCase

from booking.models import Appointment, Doctor
from .common import *


class SmokeTest(TestCase):
    """Первичная проверка работы сервиса"""

    user = doctor = apt = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(email=EMAIL, **CREDENTIALS)
        cls.doctor = Doctor.objects.create(user=cls.user, specialty=SPECIALTY)
        cls.apt = Appointment.objects.create(
            doctor=cls.doctor,
            visitor='',
            date=TODAY,
            time=TIME,
        )

    def setUp(self):
        self.client.logout()

    def test_service_running(self):
        """Проверка основных endpoint"""
        urls = (
            (URL.BOOKING, 200, None),
            (URL.ADMIN, 302, None),
            (URL.LOGIN, 200, None),
            (URL.LOGOUT, 302, None),
            (URL.SUCCESS, 200, {'id': self.apt.id}),
            (URL.schedule(self.doctor.id), 200, None),
        )

        for url, status, params in urls:
            with self.subTest(url):
                response = self.client.get(url, params)
                self.assertEqual(response.status_code, status)
