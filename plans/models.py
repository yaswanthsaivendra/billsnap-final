from django.db import models
import string
import random
from apps.models import *


def generate_code():
    length=10
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        if Plan.objects.filter(slug=code).count()==0:
            break
    return code


class Plan(models.Model):
    slug = models.CharField(max_length=20, default=generate_code, editable=False)
    app = models.ForeignKey(applists, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=800)
    duration = models.IntegerField(default=30, choices=[
            (30, '1 Month'),
            (180, '6 Months'),
            (364, '1 Year')
        ],
    )
    default_for_customer = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.title}] Plan at [Rs.{self.price}] for [{self.duration} days] in [{self.app.appname}]"
    