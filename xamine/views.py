import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from xamine.models import Order, Patient
from xamine.utils import get_setting, is_in_group


@login_required
def index(request):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/index.html')

    see_all = is_in_group(request.user, "Administrators")

    context = {}
    if see_all or is_in_group(request.user, "Physicians"):
        active_orders = Order.objects.filter(level_id__lt=4)
        complete_orders = Order.objects.filter(level_id=4)

        if not see_all:
            active_orders = active_orders.filter(doctor=request.user)
            complete_orders = complete_orders.filter(doctor=request.user)

        context['active_orders'] = active_orders
        context['complete_orders'] = complete_orders
    if see_all or is_in_group(request.user, "Receptionists"):
        # Find today's appts
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context['todays_orders'] = Order.objects.filter(level_id=1, appointment__range=(today_min, today_max))

        # Find unscheduled appts
        context['unsched_orders'] = Order.objects.filter(level_id=1, appointment__isnull=True)
    if see_all or is_in_group(request.user, "Technicians"):
        context['checked_in_orders'] = Order.objects.filter(level_id=2)
    if see_all or is_in_group(request.user, "Radiologists"):
        context['radiologist_orders'] = Order.objects.filter(level_id=3)

    return render(request, 'index.html', context)


@login_required
def order(request, order_id=None):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/order.html')

    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    context = {}

    if cur_order.level_id == 1:
        # Prepare context for template if at referral placed step
        pass
    elif cur_order.level_id == 2:
        # Prepare context for template if at checked in step
        pass
    elif cur_order.level_id == 3:
        # Prepare context for template if at imaging complete step
        pass
    elif cur_order.level_id == 4:
        # Prepare context for template if at analysis complete step
        pass
    elif cur_order.level_id == 5:
        # Prepare context for template if archived
        pass

    # Add current order to the context dict
    context["cur_order"] = cur_order

    # Define which user groups can see medical info, add to context
    medical_groups = ['Technicians', 'Radiologists', 'Physicians']
    context['show_medical'] = is_in_group(request.user, medical_groups)

    return render(request, 'order.html', context)


@login_required
def patient(request, pat_id=None):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/patient.html')

    patient = Patient.objects.get(pk=pat_id) 

    context = {
        'patient_info': patient
    }
    return render(request, 'patient.html', context)



