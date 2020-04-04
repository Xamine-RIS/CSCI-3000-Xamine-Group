from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from xamine.models import Order
from xamine.utils import get_setting, is_in_group


@login_required
def index(request):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/index.html')

    context = {}
    if is_in_group(request.user, "Physicians"):
        pass
    if is_in_group(request.user, "Receptionists"):
        pass
    if is_in_group(request.user, "Technicians"):
        pass
    if is_in_group(request.user, "Radiologists"):
        pass

    return render(request, 'index.html', context)


@login_required
def order(request, order_id=None):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/order.html')

    cur_order = Order.objects.get_object_or_404(pk=order_id)

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

    context["cur_order"] = cur_order,

    return render(request, 'order.html', context)


@login_required
def patient(request):
    if get_setting('SHOW_PROTOTYPE', 'False') == 'True':
        return render(request, 'prototype/patient.html')
