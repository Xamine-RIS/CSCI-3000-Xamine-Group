from django.db import models


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
    # TODO: include fields for patient medical information
    allergy_asthma = models.BooleanField()
    allergy_dye = models.BooleanField()
    mri_dye = models.BooleanField()
    latex = models.BooleanField()
    notes = models.TextField(null=True, blank=True)

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
            
    def __str__(self):
        return f"{self.full_name} ({self.id})"


class Order(models.Model):
    """ Model for each individual imaging order placed by doctors """
    
    # link to patient
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="orders")
    
    # Automatically record timestamp info
    added_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    # Level tracking
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, null=True, blank=True)

    # Order information
    # TODO: add fields for order info tracking (reason for visit etc)

    # Imaging information
    # TODO: use django-attachments instead of using model fields here

    # Analysis information
    # TODO: Add fields for radiologist analysis

    # Report access information
    # TODO: Add fields for patient access auth and archiving by doctor
    
    def __str__(self):
        return f"#{self.id} - {self.patient.full_name}"
