import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from booking import models
from utils import get_next_date_time, random_str


NAMES = (
    'Иван', 'Пётр', 'Николай', 'Андрей', 'Василий', 'Игорь',
    'Геннадий', 'Никита', 'Алексей', 'Александр'
)
SURNAMES = (
    'Иванов', 'Петров', 'Николаев', 'Андреев', 'Васильев', 'Жуков',
    'Рокоссовский', 'Малиновский', 'Тимошенко', 'Тухачевский'
)


class Command(BaseCommand):
    help = 'Fills the database with a demo data'

    def handle(self, *args, **options):
        user_model = get_user_model()
        doctors = []

        msg = self.style.NOTICE('Creating doctors...')
        self.stdout.write(msg)

        for number, spec in enumerate(models.Specialties, start=1):
            user = user_model.objects.create_user(
                username='demo_' + random_str(),
                first_name=random.choice(NAMES),
                last_name=random.choice(SURNAMES),
                is_staff=True,
            )
            doctor = models.Doctor.objects.create(
                user=user, specialty=spec.value
            )
            doctors.append(doctor)

        msg = self.style.SUCCESS('DONE!')
        self.stdout.write(msg)

        msg = self.style.NOTICE('Creating appointments...')
        self.stdout.write(msg)

        for _ in range(len(doctors) * 4):
            try:
                day, time = get_next_date_time()
                models.Appointment.objects.create(
                    visitor=random.choice(NAMES),
                    doctor=random.choice(doctors),
                    date=day,
                    time=time,
                )
            except ValidationError:
                pass

        msg = self.style.SUCCESS('The database successfully filled with a demo data!')
        self.stdout.write(msg)
