import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from xamine.models import Order, Patient
from xamine.forms import NewOrderForm, PatientLookupForm
from xamine.forms import PatientInfoForm, ScheduleForm, TeamSelectionForm, AnalysisForm
from xamine.utils import get_setting, is_in_group
from xamine.tasks import send_notification


@login_required
def index(request):

    see_all = is_in_group(request.user, "Administrators")

    context = {}
    if see_all or is_in_group(request.user, "Physicians"):
        active_orders = Order.objects.filter(level_id__lt=4)
        complete_orders = Order.objects.filter(level_id=4)

        if not see_all:
            active_orders = active_orders.filter(patient__doctor=request.user)
            complete_orders = complete_orders.filter(patient__doctor=request.user)

        context['active_orders'] = active_orders
        context['complete_orders'] = complete_orders

        context['patient_lookup'] = PatientLookupForm()
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
def save_order(request, order_id):

    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':

        if cur_order.level_id == 3 and is_in_group(request.user, ['Radiologists']):
            form = AnalysisForm(data=request.POST, instance=cur_order)
            if form.is_valid():

                form.save()
    
    return redirect('order', order_id=order_id)
    

@login_required
def order(request, order_id):

    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        # process submission
        
        if cur_order.level_id == 1 and is_in_group(request.user, ['Receptionists', 'Administrators']):
            form = TeamSelectionForm(data=request.POST, instance=cur_order)
            if form.is_valid():
            
                form.save()
        elif cur_order.level_id == 3 and is_in_group(request.user, ['Radiologists']):
            if request.user in cur_order.team.radiologists.all():
                form = AnalysisForm(data=request.POST, instance=cur_order)
                if form.is_valid():
                    
                    form.save()
                    cur_order.refresh_from_db()
                    cur_order.completed = request.user.get_username()
                    cur_order.completed_time = timezone.now()
                    cur_order.save()
                

                else:
                    raise Http404('bad form')
        else:
            raise Http404('bad status')

        cur_order.refresh_from_db()
        cur_order.level_id += 1
        cur_order.save()
                    
        send_notification.now(order_id)

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
        if request.user in cur_order.team.radiologists.all():
            context['analysis_form'] = AnalysisForm(instance=cur_order)
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

    if request.method == 'POST':
        form = PatientInfoForm(data=request.POST, instance=patient_rec)

        if form.is_valid():
            form.save()
        else:
            raise Http404(form.errors)

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


@login_required
def patient_lookup(request):

    dob = datetime.datetime.strptime(request.POST['birth_date'], '%m/%d/%Y').date()

    patient_list = Patient.objects.filter(birth_date=dob)

    new_form = PatientLookupForm()

    context = {
        'patient_list': patient_list,
        'date_selected': dob.strftime('%m/%d/%Y'),
        'new_patient_form': PatientInfoForm(),
        'patient_lookup': new_form,
    }
    return render(request, 'patient_lookup.html', context)


@login_required
def new_patient(request):

    if not request.method == 'POST':
        redirect('index')

    new_form = PatientInfoForm(data=request.POST)

    if new_form.is_valid():
        new_patient = new_form.save()

        new_patient.doctor_id = request.user.pk
        new_patient.save()

        return redirect('new_order', pat_id=new_patient.pk)

    else:
        context = {
            'patient_list': None,
            'date_selected': None,
            'new_patient_form': new_form,
            'show_modal': True,
        }
        return render(request, 'patient_lookup.html', context)


@login_required
def new_order(request, pat_id):

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['patient'] = pat_id

        new_form = NewOrderForm(data=form_data)

        if new_form.is_valid():
            new_order = new_form.save()
            new_order.level_id = 1
            new_order.save()

            return redirect('order', order_id=new_order.pk)
    else:
        new_form = NewOrderForm()
       
    context = {
        'new_order_form': new_form,
        'patient': Patient.objects.get(pk=pat_id),
    }
    return render(request, 'new_order.html', context)
















