from django.db import models
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from apps.models import applists
# Create your models here.
class Meta:
    abstract = True

class customer(models.Model):

    app = models.ForeignKey(applists, on_delete=models.CASCADE)

    #utility details
    utility_name = models.CharField(max_length=200, null=True, blank=True)
    utility_short_name= models.CharField(max_length=50, null=True, blank=True)
    utility_state= models.CharField(max_length=50, null=True, blank=True)
    utility_district= models.CharField(max_length=50, null=True, blank=True)
    utility_country= models.CharField(max_length=50, null=True, blank=True)
    utility_postalcode= models.CharField(max_length=20, null=True, blank=True)
    utility_address=models.TextField(max_length=200, null=True, blank=True)

    #contact details
    contact_person= models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField(max_length=50, null=True, blank=True)
    contact_phnum = models.CharField(max_length=15, null=True, blank=True)
    contact_mobile= models.CharField(max_length=15, null=True, blank=True)
    contact_designation= models.CharField(max_length=100, null=True, blank=True)
    contact_landline= models.CharField(max_length=20, null=True, blank=True)

    #emeergency contact details
    emergency_person=models.CharField(max_length=200, null=True, blank=True)
    emergency_altperson=models.CharField(max_length=200, null=True, blank=True)
    emergency_mobile=models.CharField(max_length=200, null=True, blank=True)
    emergency_altmobile=models.CharField(max_length=200, null=True, blank=True)
    emergency_officeaddress=models.TextField(max_length=200,null=True,blank=True)
    emergency_altofficeaddress=models.TextField(max_length=200,null=True,blank=True)


    info_created_at = models.DateTimeField(auto_now_add=True)
    info_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.utility_name

class csvs(models.Model):
    LatD=models.CharField(max_length=50, null=True, blank=True)
    LatM=models.CharField(max_length=50, null=True, blank=True)
    LatS=models.CharField(max_length=50, null=True, blank=True)
    NS=models.CharField(max_length=50, null=True, blank=True)
    LonD=models.CharField(max_length=50, null=True, blank=True)
    LonM=models.CharField(max_length=50, null=True, blank=True)
    LonS=models.CharField(max_length=50, null=True, blank=True)
    EW=models.CharField(max_length=50, null=True, blank=True)
    City=models.CharField(max_length=50, null=True, blank=True)
    State=models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.State)

class settings(models.Model):
    custlis=models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return str(self.State)