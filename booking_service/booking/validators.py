from datetime import date
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def date_validator(value):
    """Проверка соответствия даты записи"""
    today = date.today()
    code = 'bad_date'

    if value.isoweekday() > 5:
        raise ValidationError(_('Дата записи не может быть выходным днём'), code=code)
    if value < today:
        raise ValidationError(_('Дата записи не может быть раньше текущего дня'), code=code)
    if value.year > today.year + 1:
        raise ValidationError(_('Дата записи не может быть назначена далее следующего года'), code=code)

    return value


def name_validator(value):
    """Проверка соответствия имени пациента"""
    pattern = r"^[а-яА-ЯёЁa-zA-Z -]{3,}$"
    if not re.fullmatch(pattern, value):
        raise ValidationError(_('Имя и фамилия указаны некорректно'), code='bad_fio')
    return value
