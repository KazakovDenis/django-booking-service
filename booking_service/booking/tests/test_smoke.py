from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from booking.models import Appointment, Doctor
from .common import *


class SmokeTest(TestCase):
    """Первичная проверка работы сервиса"""

    user = doctor = apt = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        date, time = get_next_date_time()
        cls.user = User.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.doctor = Doctor.objects.create(user=cls.user, specialty=SPECIALTY)
        cls.apt = Appointment.objects.create(
            doctor=cls.doctor,
            visitor=random_str(),
            date=date,
            time=time,
        )

    def setUp(self):
        self.client.logout()

    def test_service_running(self):
        """Проверка основных endpoint"""
        test_data = (
            (URL.BOOKING, 200, None),
            (URL.ADMIN, 302, None),
            (URL.LOGIN, 200, None),
            (URL.LOGOUT, 302, None),
            (URL.SUCCESS, 200, {'id': self.apt.id}),
            (URL.schedule(self.doctor.id), 200, None),
        )

        for url, status, params in test_data:
            with self.subTest(url):
                response = self.client.get(url, params)
                self.assertEqual(response.status_code, status)

    def test_auth(self):
        """Проверка аутентификации"""
        response = self.client.get(URL.ADMIN, follow=True)
        self.assertContains(response, _('Войти'))

        self.client.login(**CREDENTIALS)
        response = self.client.get(URL.ADMIN)
        self.assertContains(response, _('Добро пожаловать'))
