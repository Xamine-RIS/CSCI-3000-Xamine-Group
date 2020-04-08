from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Level(models.Model):
    """ Model to define different points in order workflow """
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class AppSetting(models.Model):
    """ Defines settings that can be turned on and off """
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Patient(models.Model):
    """ Model to track the patient and their history """

    # Personal information
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128)
    email_info = models.EmailField()
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=10)

    # Medical information
    allergy_asthma = models.BooleanField()
    allergy_xraydye = models.BooleanField()
    allergy_mridye = models.BooleanField()
    allergy_latex = models.BooleanField()

    notes = models.TextField(null=True, blank=True)

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
            
    def __str__(self):
        return f"{self.full_name} ({self.id})"


class ModalityOptions(models.Model):   #temp
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Model for each individual imaging order placed by doctors """

    # patient info
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="orders")
    appointment = models.DateTimeField(null=True, blank=True)

    # Automatically record timestamp info
    added_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    # Level tracking
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Order information
    visit_reason = models.CharField(max_length=128, null=True, blank=True)  # temp
    imaging_needed = models.CharField(max_length=128, null=True, blank=True)  # temp
    modality = models.ForeignKey(ModalityOptions, on_delete=models.SET_NULL, null=True, blank=True)  # temp

    # Analysis information
    report = models.TextField(null=True, blank=True)

    # Report access information
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # TODO: Add fields for patient access auth and archiving by doctor
    
    def __str__(self):
        return f"#{self.id} - {self.patient.full_name}"


def image_path(instance, filename):
    timestamp = timezone.now().strftime('%f')

    return f"ris/{instance.order.id}/{timestamp}-{filename}"


class Image(models.Model):
    """ Model for the actual Image to be associated with an Order """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    label = models.CharField(max_length=30)
    image = models.FileField(upload_to=image_path)
    user = models.CharField(max_length=30)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} for order # {self.order.id}"
