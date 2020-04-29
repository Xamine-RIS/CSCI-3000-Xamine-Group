from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from xamine.models import OrderKey
import random
import string

from xamine.tasks import send_email


@api_view(['GET'])
def patient_email(request, order_id):
    try:
        current_key = OrderKey.objects.get_or_create(order_id=order_id)[0]

        key = randomString()

        current_key.secret_key = key
        current_key.save()

        url = f"{request.get_host()}{reverse('public_order')}?key={key}"
        to_email = current_key.order.patient.email_info

        html_content = "Imaging report has been emailed to you: <br><br>" + url

        send_email([to_email], 'xamineinc@gmail.com', 'RIS Report is Ready', html_content)

        # send_mail(
        #     'RIS Report is Ready',
        #     f'Navigate here to view: {url}',
        #     'xamineinc@gmail.com',
        #     [to_email],
        #     fail_silently=False,
        # )

        return_data = {
            'status': 'ok',
            'message': 'Email sent!',
            'link': url if settings.DEBUG else None,
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
