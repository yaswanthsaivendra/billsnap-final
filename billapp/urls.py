from django.urls import path, include
from . import views
from accounts import views as acc_views
from django.contrib.auth import views as a_views

urlpatterns = [
    path('', views.index, name='index'),
    path('custdash/',views.dashcustomer,name='custdash'),
    path('customer-plans/',views.customer_plans,name='customer-plans'),
    path('customer-notifications/',views.customer_notifications,name='customer-notifications'),
    path('send/',views.sending,name='send'),
    path('settings/', views.sett_ings, name='settings'),
    path('dashboard/', views.dashboard, name='dash'),
    path('apps/', include('apps.urls')),
]