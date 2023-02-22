from django.urls import path, include
from .views import *
from django.contrib.auth import views as a_views

app_name='groups'

urlpatterns = [
    path('panel/<str:slug>', groups_panel, name='groups-panel'),
    path('delete-group/<str:slug>/<str:appslug>', delete_group, name='delete-group'),
    path('group/<str:slug>/<str:groupslug>', show_group, name='group'),
    path('add-member/<str:groupslug>', add_customer_to_group, name='add-member'),
    path('remove-member/<str:groupslug>', remove_customer_from_group, name='remove-member'),
    # path('update-group/<str:slug>/<str:groupslug>', update_user_group, name='update-group'),
    path('plangroup/<str:slug>/<str:plangroupslug>', show_plan_group, name='plangroup'),

]