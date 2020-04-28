from sendgrid import SendGridAPIClient, Mail

from xamine.models import AppSetting, Patient
from datetime import datetime
from django.http import Http404

import requests

def send_mailgun_email(recip_list):
    if isinstance(recip_list, str):
        recip_list = [recip_list]

    return requests.post(
        "https://api.mailgun.net/v3/xaminemail.msb.dev",
        auth=("api", "bac0805840288ae22c69a0603af0f77b-b3780ee5-716f5d4a"),
        data={"from": "XamineRIS <mailgun@xaminemail.msb.dev>",
			"to": recip_list,
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})


def send_sendgrid_email(recipient, subject, html_msg):
    message = Mail(
        from_email='noreply@xamine.msb.dev',
        to_emails=recipient,
        subject=subject,
        html_content=html_msg)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


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
    thumbnail_exts = ['jpg', 'png', 'bmp']

    thumbnails = []
    for image in images:
        ext = image.image.path.split('.')[-1]
        if ext.lower() in thumbnail_exts:
            thumbnails.append(image)

    return thumbnails
