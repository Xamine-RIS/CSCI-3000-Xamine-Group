from xamine.models import AppSetting


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


def get_image_files(images):
    # List of thumbanilable extensions
    thumbnail_exts = ['jpg', 'png', 'bmp']

    # For each image whose type is listed above, add to our thumbnail list
    thumbnails = []
    for image in images:
        ext = image.image.path.split('.')[-1]
        if ext.lower() in thumbnail_exts:
            thumbnails.append(image)

    # Return thumbnail list established above
    return thumbnails

