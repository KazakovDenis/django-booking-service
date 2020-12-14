from django.urls import reverse


USERNAME = 'test_user'
PASSWORD = 'sup3rs3cr3tp@$$'
EMAIL = 'test@email.com'
CREDENTIALS = {'username': USERNAME, 'password': PASSWORD}
SPECIALTY = 'therapist'
FORM_DATE_FMT = '%d.%m.%Y'


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
