from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Notification)

class NotificationsInline(admin.StackedInline):
    model = Notification
    extra = 1