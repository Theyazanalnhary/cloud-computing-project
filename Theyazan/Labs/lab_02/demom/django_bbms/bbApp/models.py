from django.db import models
from django.db.models import Sum
from django.utils import timezone

# Create your models here.
class Blood_Group(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default = 1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_total_volume(self):
        try:
            total_donation = Donation.objects.filter(blood_group = self).aggregate(Sum('donation_volume'))['donation_volume__sum']
            if total_donation is None:
                total_donation = 0
        except:
            total_donation = 0
        try:
            total_request = Request.objects.exclude(status = 4).filter(blood_group = self).aggregate(Sum('volume'))['volume__sum']
            if total_request is None:
                total_request = 0
        except:
            total_request = 0
        return (total_donation - total_request) / 1000

class Donation(models.Model):
    blood_group = models.ForeignKey(Blood_Group, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=500)
    donor_contact = models.CharField(max_length=250)
    donor_email = models.CharField(max_length=250)
    donor_address = models.TextField(blank=True, null=True)
    donor_gender = models.CharField(max_length=30, choices = (('Male' ,'Male'),('Female' ,'Female')))
    transfusion_date = models.DateField()
    donation_volume = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.donor_name} - ({self.blood_group.name})"

class Request(models.Model):
    blood_group = models.ForeignKey(Blood_Group, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=500)
    patient_gender = models.CharField(max_length=30, choices = (('Male' ,'Male'),('Female' ,'Female')))
    volume = models.FloatField(default=0)
    physician_name = models.CharField(max_length=500, blank=True,null=True)
    status = models.CharField(max_length=2, choices = (('1' ,'Pending'),('2' ,'Approved'),('3' ,'Handed-Over'),('4' ,'Denied')))
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - ({self.blood_group.name})"
    