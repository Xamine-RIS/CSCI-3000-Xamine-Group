from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from xamine.models import OrderKey, AppSetting
import random
import string

from xamine.tasks import send_email


@api_view(['GET'])
def patient_email(request, order_id):
    """ Handles sending email to patient to view order """

    # Establish where the app is hosted
    host = "abisalimi.pythonanywhere.com/"

    # attempt to send email
    try:
        # Either create or update the key for this order
        current_key = OrderKey.objects.get_or_create(order_id=order_id)[0]

        # Grab a new random string for our key
        key = random_string()

        # Assign new key to the OrderKey and save
        current_key.secret_key = key
        current_key.save()

        # Establish our URL and recipient, the patient's email
        url = f"https://{host}{reverse('public_order')}?key={key}"
        to_email = current_key.order.patient.email_info

        # Set up our message content
        html_content = "Imaging report has been emailed to you: <br><br>" + url

        if AppSetting.get_setting('EMAIL_TOGGLE') == 'True':
            # Send patient our email
            send_email([to_email], 'xamineinc@gmail.com', 'RIS Report is Ready', html_content)
            message = 'Email Sent!'
        else:
            message = 'Link created!'

        # Return JSON to confirm success
        return_data = {
            'status': 'ok',
            'message': message,
            'link': url,
        }
        return Response(return_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return JSON to express failure
        return_data = {
            'status': 'fail',
            'message': f'Email not sent!',
        }
        return Response(return_data, status=status.HTTP_400_BAD_REQUEST)


def random_string(string_length=128):
    """ Gets random string of desired length """
    # Get list of all lowercase and uppercase letters and return the desired number of them randomly
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(string_length))
