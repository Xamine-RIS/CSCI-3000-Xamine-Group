from django.db import models

class Patient(models.Model):
    """ Model to track the patient and their history """
    
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128)
    
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
    
    # link to patient to be images
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="orders")
    
    # Automatically record timestamp info
    added_on = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"#{self.id} - {self.patient.full_name}"
