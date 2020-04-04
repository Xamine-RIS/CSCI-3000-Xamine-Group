from xamine.models import AppSetting


def get_setting(name):
    setting = AppSetting.objects.get(pk=name)
    return setting.value


def is_in_group(user, group):
    return user.groups.filter(name=group).exists()