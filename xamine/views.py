import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from xamine.models import Order, Patient
from xamine.forms import PatientInfoForm, ScheduleForm, TeamSelectionForm
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
def order(request, order_id):

    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        # process submission
        form = TeamSelectionForm(data=request.POST, instance=cur_order)
        
        if cur_order.level_id == 1 and is_in_group(request.user, ['Receptionists', 'Administrators']) and form.is_valid():
            form.save()

            cur_order.level_id = 2
            cur_order.save()

        # TODO: send notification email

    context = {}

    if cur_order.level_id == 1:
        # Add scheduler form if not yet checked in
        context['schedule_form'] = ScheduleForm(instance=cur_order)
        context['checkin_form'] = TeamSelectionForm(instance=cur_order)
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

    patient_rec = Patient.objects.get(pk=pat_id)

    context = {
        'patient_info': patient_rec,
        'form': PatientInfoForm(instance=patient_rec),
        'active_orders': patient_rec.orders.filter(level_id__lt=4),
        'complete_orders': patient_rec.orders.filter(level_id__gte=4),
    }
    return render(request, 'patient.html', context)


@login_required
def schedule_order(request, order_id):

    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        if request.POST['appointment']:
            appt = datetime.datetime.strptime(request.POST['appointment'], '%m/%d/%Y %I:%M %p')
            twohrslater = appt + datetime.timedelta(hours=2)

            conflict = Order.objects.filter(appointment__gte=appt, appointment__lt=twohrslater).exists()
        else:
            appt = None
            conflict = False

        if not conflict:
            order.appointment = appt
            order.save()
        else:
            # TODO display error
            raise Http404('date conflict')

    return redirect('order', order_id=order_id)
