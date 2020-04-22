from xamine.models import AppSetting
from datetime import datetime
from django.http import Http404


def get_setting(name, default=None):
    """ Get the setting from the database """

    # We look for the provided setting.
    # If it's not found, we return the default, if given.
    # If not, we return None
    try:
        return AppSetting.objects.get(name=name).value
    except AppSetting.DoesNotExist:
        return default


def is_in_group(user, group):
    """ Check if the supplied user is in the group list """

    # If we're provided a single group name, convert it to a list.
    # This allows us to pass both a single group and a list to check against.
    if isinstance(group, str):
        group = [group]

    return user.groups.filter(name__in=group).exists()


def get_patients_from_dob(dob, user):
    if is_in_group(user, 'Physicians'):
        patient_list = Patient.objects.all()
    elif is_in_group(user, ['Administrators', 'Radiologists', 'Receptionists', 'Technicians']):
        patient_list = Patient.objects.all()
    else:
        raise Http404('bad auth')