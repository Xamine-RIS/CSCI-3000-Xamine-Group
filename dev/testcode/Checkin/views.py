from django.views.generic import TemplateView
from django.shortcuts import render, redirect

from polls.forms import CheckinForm
from polls.models import CheckinModel

class CheckinView(TemplateView):
template_name='patient copy.html'

def get(self, request)
    form = CheckinForm
    information = CheckinModel.objects.all()
    args = {'form': form, 'information': information}
    return render(request, self.template_name, args)
def post(self, request)
    form = CheckinForm(request.POST)
    if form.is_valid:
        form.save()
        info = form.cleaned_data('FirstName', 'LastName', 'DOB', 'PhoneNumber',
       'Email', 'Asthma', 'XrayDye', 'MRIDye', 'Latex',
       'AdditionalInfo')
       form = CheckinForm()
       return redirect(CheckinForm:CheckinForm)

    args = ('form': form, 'info': info)
    return render(request, self.template_name, args)
