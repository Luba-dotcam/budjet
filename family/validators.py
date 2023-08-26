from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if len(value) < 4:
        raise ValidationError(
            _('Username must be at least 4 characters long.'),
            code='username_length'
        )
