from django.db import models
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from plans.models import *

# Create your models here.
User._meta.get_field('email')._unique = True

def current_year():
        return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+10)(value)

def get_unique_string(body, time):
    s = str(body)+str(time)
    result_str = hashlib.sha1(s.encode()).hexdigest()[:10]
    return result_str

gender_choices = (('M', 'MALE'),
('F', 'FEMALE'),
('O', 'OTHER'))

status_choices = [
    ('a', 'admin'),
    ('c', 'customer')
]
from apps.models import applists

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    apps=models.ManyToManyField(applists,related_name='apps')
    status = models.CharField(choices=status_choices, max_length=20, default='c')
    full_name = models.CharField(max_length=100, blank=True, null=True)


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

    se_coins= models.IntegerField(null=True, default=999, blank=True)
    slug = models.SlugField(max_length=200, editable=False, null=True, blank=True)

    admin=models.BooleanField(default=False)
    plans = models.ManyToManyField(Plan)
    plan_active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        self.slug = slugify(self.user.username)
        super(Profile, self).save()

    def courseprofile(self):
        return self.course_profile.all()

class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_notifications')
    image = models.ImageField(upload_to='notifications')
    body = models.TextField()
    url = models.URLField(null=True, blank=True)
    url_name = models.CharField(max_length=255, default='View', null=True, blank=True)
    notified_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.profile.user.username + ' ' + self.body[0:15]

    def save(self, *args, **kwargs):
        super(Notification, self).save()
        self.slug = slugify(get_unique_string(self.body, self.notified_time))
        super(Notification, self).save()

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    log = models.CharField(max_length=300)
    amount = models.IntegerField(default=0)
    code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"USER [{self.user.username}] LOG [{self.log}] DATE [{self.date}] AMOUNT [{self.amount}]"

# Create your views here.
def create_history(user, to_plan, from_plan=None, upgrade=False):
    if upgrade:
        history = TransactionHistory.objects.get(user=user, code=from_plan.slug)
        today = datetime.date.today()
        completed_days = (today - history.date).days
        payment_per_day = from_plan.price / from_plan.duration
        payment_adv = (from_plan.duration - completed_days)*payment_per_day
        price_to_pay = to_plan.price - payment_adv
        
        log = f"User [{user.username}] Upgraded to Plan [{to_plan}] from Plan [{from_plan}]"
        TransactionHistory.objects.create(user=user, log=log, amount=price_to_pay, code=to_plan.slug)
    else :
        log = f"User [{user.username}] Subscribed to Plan [{to_plan}]"
        TransactionHistory.objects.create(user=user, log=log, amount=to_plan.price, code=to_plan.slug)
