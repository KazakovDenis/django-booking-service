from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import date_validator, name_validator


class Specialties(models.TextChoices):
    """Специальности врачей"""
    SURGEON = 'surgeon', _('хирург')
    DENTIST = 'dentist', _('стоматолог')
    THERAPIST = 'therapist', _('терапевт')
    NEUROLOGIST = 'neurologist',  _('невролог')
    OPHTHALMOLOGIST = 'ophthalmologist',  _('офтальмолог')
    PSYCHOTHERAPIST = 'psychotherapist',  _('психотерапевт')
    OTOLARYNGOLOGIST = 'otolaryngologist',  _('отоларинголог')


class Doctor(models.Model):
    """Врач"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(_('специальность'), max_length=255, choices=Specialties.choices)

    class Meta:
        verbose_name = _('врач')
        verbose_name_plural = _('врачи')
        ordering = ['specialty', 'user']

    def full_name(self):
        return f'{self.user.last_name} {self.user.first_name}'
    full_name.short_description = _('Фамилия и имя врача')
    full_name = property(full_name)

    @property
    def spec_label(self):
        return str(Specialties(self.specialty).label)

    def __str__(self):
        return f'{self.spec_label} {self.full_name}'


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
    visitor = models.CharField(_('пациент'), max_length=255, validators=[name_validator])
    date = models.DateField(_('дата приёма'), validators=[date_validator])
    time = models.IntegerField(_('время приёма'), choices=ConsultingHours.choices)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name=_('врач'),
        related_name='appointments',
    )

    class Meta:
        verbose_name = _('приём у врача')
        verbose_name_plural = _('приёмы у врача')
        unique_together = ('date', 'time', 'doctor')
        ordering = ['date', 'time', 'doctor']

    @property
    def str_time(self):
        return f'{self.time}:00'

    def __str__(self):
        return f'{self.doctor} @ {self.str_time} {self.date}'
