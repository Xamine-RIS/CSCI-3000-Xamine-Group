from django import forms

from xamine.models import Patient

class PatientInfoForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name','last_name','email_info','birth_date','phone_number',
            'allergy_asthma','allergy_xraydye','allergy_mridye','allergy_latex','notes'
            ]





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