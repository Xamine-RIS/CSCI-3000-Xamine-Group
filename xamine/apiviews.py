from django.shortcuts import render
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from xamine.models import Order, Patient, OrderKey
import random
import string


@api_view(['GET'])
def patient_email(request, order_id):
    try:
        current_key = OrderKey.objects.get_or_create(order_id=order_id)[0]

        print(current_key)

        current_key.secret_key = randomString()
        current_key.save()

        url = f"{request.get_host()}"
        to_email = current_key.order.patient.email_info

        send_mail(
            'RIS Report is Ready',
            f'<a href="{url}">Click here to view</a>',
            'donotreply@xaminegroup.pythonanywhere.com',
            [to_email],
            fail_silently=False,
        )

        return_data = {
            'status': 'ok',
            'message': 'Email sent!'
        }

        return Response(return_data, status=status.HTTP_201_CREATED)
    except:
        return_data = {
            'status': 'fail',
            'message': 'Email not sent!'
        }
        return Response(return_data, status=status.HTTP_400_BAD_REQUEST)


def randomString(stringLength=128):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
