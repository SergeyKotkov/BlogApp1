from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import date
from django.utils import timezone


def validate_password(value):
    if len(value) < 8:
        raise ValidationError(_('Password must be at least 8 characters long'))
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must include at least one number'))
    if not any(char.isupper() for char in value):
        raise ValidationError(_('Password must include at least one uppercase letter'))
    if not any(char.islower() for char in value):
        raise ValidationError(_('Password must include at least one lowercase letter'))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(_('Password must include at least one special character'))


def validate_email_domain(value):
    domain = value.split('@')[-1].lower()
    if domain not in ['mail.ru', 'yandex.ru']:
        raise ValidationError(_('Only mail.ru and yandex.ru domains are allowed.'))


def validate_author_age(birth_date):
    if not isinstance(birth_date, date):
        raise ValidationError(_('Invalid date format for birth_date'))

    today = timezone.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError(_('Author must be at least 18 years old.'))


def validate_forbidden_words(value):
    forbidden_words = ['ерунда', 'глупость', 'чепуха']
    value_lower = value.lower()
    for word in forbidden_words:
        if word in value_lower:
            raise ValidationError(_('Title contains forbidden word: %(word)s') % {'word': word})