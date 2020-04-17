from django import forms

from intl_tel_input.widgets import IntlTelInputWidget
from xamine.models import Patient

from bootstrap_datepicker_plus import DatePickerInput

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





"""
# Personal information
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128)
    email_info = models.EmailField()
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=10)


    # Medical information
    allergy_asthma = models.BooleanField()
    allergy_dye = models.BooleanField()
    mri_dye = models.BooleanField()
    latex = models.BooleanField()
    notes = models.TextField(null=True, blank=True)
"""