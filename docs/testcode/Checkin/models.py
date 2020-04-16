from django.db import models

class CheckinModel(models.Model):
    Boolean_Choices = ((True, 'Yes'), (False, 'No'))
    FirstName = models.CharField(max_length=25)
    LastName = models.CharField(max_length=25)
    DOB = models.CharField(max_length=25)
    PhoneNumber = models.CharField(max_length=10)
    Email = models.CharField(max_length=50)
    Asthma = models.BooleanField(choices=Boolean_Choices)
    XrayDye = models.BooleanField(choices=Boolean_Choices)
    MRIDye = models.BooleanField(choices=Boolean_Choices)
    Latex = models.BooleanField(choices=Boolean_Choices)
    AdditionalInfo = models.CharField(max_length=500)
