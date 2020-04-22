from django import forms

from intl_tel_input.widgets import IntlTelInputWidget
from xamine.models import Patient, Order

from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput

yesnoch = (
    (False, 'No'),
    (True, 'Yes'),
)


class PatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name', 'email_info', 'birth_date', 'phone_number',
            'allergy_asthma', 'allergy_xraydye', 'allergy_mridye', 'allergy_latex', 'notes'
            ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email_info': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'birth_date': DatePickerInput(format='%m/%d/%Y', options={"useCurrent": False},
                                          attrs={'placeholder': 'mm/dd/yyyy'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control input-phone', 'autocomplete': 'off'}),
            'allergy_asthma': forms.Select(attrs={'class': 'form-control'}, choices=yesnoch),
            'allergy_xraydye': forms.Select(attrs={'class': 'form-control'}, choices=yesnoch),
            'allergy_mridye': forms.Select(attrs={'class': 'form-control'}, choices=yesnoch),
            'allergy_latex': forms.Select(attrs={'class': 'form-control'}, choices=yesnoch),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off', 'rows': '3'}),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['appointment']

        widgets = {
            'appointment': DateTimePickerInput(format='%m/%d/%Y %I:%M %p', options={"useCurrent": True},  
                                                attrs={'placeholder': 'mm/dd/yyyy'})
        }


class TeamSelectionForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['team']

        widgets = {
            'team': forms.Select(attrs={'class': 'form-control'})
        }


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['report']

        widgets = {
            'report': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off', 'rows': '6'}),
        }

