from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Specialties(models.TextChoices):
    """Специальности врачей"""
    DENTIST = 'dentist', _('стоматолог')
    SURGEON = 'surgeon', _('хирург')
    THERAPIST = 'therapist', _('терапевт')


class Doctor(models.Model):
    """Врач"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(_('специальность'), max_length=255, choices=Specialties.choices)

    class Meta:
        verbose_name = _('врач')
        verbose_name_plural = _('врачи')
        ordering = ['specialty', 'user']

    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    full_name.short_description = _('Имя и фамилия врача')
    property(full_name)

    def __str__(self):
        spec = Specialties(self.specialty).label
        return f'[{spec}] {self.full_name}'


class ConsultingHours(models.IntegerChoices):
    """Часы приёма"""
    HOUR9 = 9, '09:00'
    HOUR10 = 10, '10:00'
    HOUR11 = 11, '11:00'
    HOUR12 = 12, '12:00'
    HOUR13 = 13, '13:00'
    HOUR14 = 14, '14:00'
    HOUR15 = 15, '15:00'
    HOUR16 = 16, '16:00'
    HOUR17 = 17, '17:00'


class Appointment(models.Model):
    """Приём у врача"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    visitor = models.CharField(_('пациент'), max_length=255)
    date = models.DateField(_('дата приёма'))
    time = models.IntegerField(_('время приёма'), choices=ConsultingHours.choices)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name=_('врач'),
        related_name='appointments',
    )

    class Meta:
        verbose_name = _('приём у врача')
        verbose_name_plural = _('приёмы у врачей')
        unique_together = ('date', 'time', 'doctor')
        ordering = ['date', 'time', 'doctor']

    def get_time(self):
        return f'{self.time}:00'

    def __str__(self):
        time = self.get_time()
        return f'{self.doctor} @ {self.date} {time}'
