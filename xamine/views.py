from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from xamine.models import Patient


@login_required
def index(request, patid=None):

    if patid:
        patient = Patient.objects.get(pk=patid)
        message = "Patient: " + patient.first_name + ' ' + patient.last_name
    else:
        message = 'No Patient Selected'

    context = {
        'message': message
    }
    return render(request, 'base/coming_soon.html', context)
