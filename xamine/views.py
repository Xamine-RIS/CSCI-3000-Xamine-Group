import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone

from xamine.models import Order, Patient
from xamine.forms import ImageUploadForm
from xamine.forms import NewOrderForm, PatientLookupForm
from xamine.forms import PatientInfoForm, ScheduleForm, TeamSelectionForm, AnalysisForm
from xamine.utils import is_in_group
from xamine.tasks import send_notification


@login_required
def index(request):
    """ Displays dashboard tables, depending on group membership of logged in user. """

    # Determine if current user can see all sections
    see_all = is_in_group(request.user, "Administrators")

    # Set up empty context to pass to template
    context = {}

    # Check if administrator or physician
    if see_all or is_in_group(request.user, "Physicians"):
        # Grab active orders and completed orders from database
        active_orders = Order.objects.filter(level_id__lt=4)
        complete_orders = Order.objects.filter(level_id=4)

        # If we are not an administrator, limit active and complete orders to
        # the logged in users' patients.
        if not see_all:
            active_orders = active_orders.filter(patient__doctor=request.user)
            complete_orders = complete_orders.filter(patient__doctor=request.user)

        # Add the orders we grabbed to our template context
        context['active_orders'] = active_orders
        context['complete_orders'] = complete_orders

        # Add the patient lookup form to our context
        context['patient_lookup'] = PatientLookupForm()

    # Check if administrator or receptionist
    if see_all or is_in_group(request.user, "Receptionists"):
        # Find today's appts. To filter by today's appointments, we find the datetime for today at midnight,
        # and today at 11:59 PM. We then find all appts between those two ranges. Then we add it to the context.
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context['todays_orders'] = Order.objects.filter(level_id=1, appointment__range=(today_min, today_max))

        # Find unscheduled appointments
        context['unsched_orders'] = Order.objects.filter(level_id=1, appointment__isnull=True)

    # Check if administrator or technician
    if see_all or is_in_group(request.user, "Technicians"):
        # Pass into context all checked in orders for any team where the logged in user is a technician.
        context['checked_in_orders'] = Order.objects.filter(level_id=2, team__technicians=request.user)

    if see_all or is_in_group(request.user, "Radiologists"):
        # Pass into context all imaging complete orders for teams where logged in user is a radiologist.
        context['radiologist_orders'] = Order.objects.filter(level_id=3, team__radiologists=request.user)

    # Render the dashoboard with any context we've passed in.
    return render(request, 'index.html', context)


@login_required
def save_order(request, order_id):
    """ Saves radiology report but does not complete order """

    # Attempt to grab order via order_id from url. 404 if not found.
    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    # Ensure request method is POST
    if request.method == 'POST':
        # Check if Order is at radiologist level and request user is a radiologist and is on the order's team.
        if cur_order.level_id == 3 and is_in_group(request.user, ['Radiologists']):
            if request.user in cur_order.team.radiologists.all():
                # Set up form with our data and save if valid
                form = AnalysisForm(data=request.POST, instance=cur_order)
                if form.is_valid():

                    form.save()

    # Always redirect to specified order
    return redirect('order', order_id=order_id)
    

@login_required
def upload_file(request, order_id):
    """ Uploads file to specified order """

    # Check if we have a POST request
    if request.method == 'POST':
        # Create a malleable copy of our POST data, add the order id to it.
        data = request.POST.copy()
        data['order'] = order_id

        # Check if our form is valid
        form = ImageUploadForm(data, request.FILES)
        if form.is_valid():
            # File is saved
            new_image = form.save()

            # Record who uploaded the file
            new_image.user = request.user.get_username()
            new_image.save()

    # Regardless of the result of our post request, reload order page
    return redirect('order', order_id=order_id)


@login_required
def order(request, order_id):

    # Attempt to grab order via order_id from url. 404 if not found.
    try:
        cur_order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404

    # Check if we have a POST request
    if request.method == 'POST':

        # Check if level and permissions for the logged in user are both receptionists or admins
        if cur_order.level_id == 1 and is_in_group(request.user, ['Receptionists', 'Administrators']):

            # Assign POST data to selection form, check if it's valid, and save if so
            form = TeamSelectionForm(data=request.POST, instance=cur_order)
            if form.is_valid():
                form.save()

        # Check if level and permissions for the logged in user are both technicians
        elif cur_order.level_id == 2 and is_in_group(request.user, ['Technicians', 'Radiologists']):
                pass

        # Check if level and permissions for the logged in user are both radiology
        elif cur_order.level_id == 3 and is_in_group(request.user, ['Radiologists']):
            if request.user in cur_order.team.radiologists.all():
                form = AnalysisForm(data=request.POST, instance=cur_order)
                if form.is_valid():

                    #
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

    if cur_order.level_id == 1 and is_in_group(request.user, ['Receptionists', 'Administrators']):
        # Add scheduler form if not yet checked in
        context['schedule_form'] = ScheduleForm(instance=cur_order)
        context['checkin_form'] = TeamSelectionForm(instance=cur_order)
    elif cur_order.level_id == 2 and is_in_group(request.user, ['Technicians', 'Radiologists']):
        # Prepare context for template if at checked in step
        if request.user in cur_order.team.radiologists.all() | cur_order.team.technicians.all():
            context['image_form'] = ImageUploadForm(instance=cur_order)
    elif cur_order.level_id == 3 and is_in_group(request.user, ['Radiologists']):
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
















