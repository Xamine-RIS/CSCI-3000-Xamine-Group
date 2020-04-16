from django.db import models

class Inbox(models.Model):
    patient_name = models.CharField(max_length= 200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.patient_name

class Choice(models.Model):
    results = models.ForeignKey(Inbox, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    send = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
