from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth import views as a_views

urlpatterns = [
    path('subscribe-plan/<str:slug>', subscribe, name='subscribe-plan'),
    path('upgrade-to/<str:slug>', upgrade_to, name='upgrade-to'),
    path('panel/<str:slug>', plans_panel, name='plans-panel'),
    path('delete-plan/<str:slug>/<str:planslug>/', delete_plan, name='delete-plan'),
    path('plan/<str:slug>/<str:planslug>', show_plan, name='plan'),
    path('update-plan/<str:profileslug>/<str:planslug>/', update_user_plan, name='update-plan'),
]
