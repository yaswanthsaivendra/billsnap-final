from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
import hashlib
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def get_unique_string(body, time):
    s = str(body)+str(time)
    result_str = hashlib.sha1(s.encode()).hexdigest()[:10]
    return result_str

class applists(models.Model):

    author= models.ForeignKey(User, on_delete=models.CASCADE)
    appname=models.CharField(verbose_name='App name',primary_key=True,max_length=50,unique=True,null=False)
    appimg=models.ImageField(upload_to = 'app_images',null=True,blank=True)
    date_published= models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, null=True, unique=True, editable=False)
    is_billing = models.BooleanField(default=True)

    def __str__(self):
        return str(self.slug)

    def save(self, *args, **kwargs):
        super(applists, self).save()
        self.slug = slugify(self.appname)
        super(applists, self).save()

    def get_absolute_url(self):
        return reverse('apps')
