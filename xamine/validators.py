import datetime

from django.core.exceptions import ValidationError


def validate_file_size(value):
    """ validates size of image uploads. """
    filesize = value.size

    if filesize > 2000000000:
        raise ValidationError("The maximum file size that can be uploaded is 2GB")
    else:
        return value


def check_past_date(value):
    if value > datetime.date.today():
        raise ValidationError("Birthdate must be in the past.")
    else:
        return value