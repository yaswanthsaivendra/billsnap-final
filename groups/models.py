from django.db import models
from accounts.models import *
from apps.models import *

# Create your models here.

def generate_code_group():
    length=10
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        if Group.objects.filter(slug=code).count()==0:
            break
    return code

class Group(models.Model):
    slug = models.CharField(max_length=20, default=generate_code_group, editable=False)
    members = models.ManyToManyField(Profile)
    title = models.CharField(max_length=200)
    app = models.ForeignKey(applists, on_delete=models.CASCADE)
    description = models.TextField(max_length=800)
    
    def __str__(self):
        return self.title
    

