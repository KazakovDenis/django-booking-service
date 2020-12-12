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
            ('/', 200),
            ('/admin/', 302),
            ('/admin/login/', 200),
            ('/admin/logout/', 302),
            (f'/schedule/{self.doctor.id}', 200),
            (f'/success/?id={self.apt.id}', 200),
        )

        for url, status in urls:
            with self.subTest(url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)
