from django.urls import path, include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('estimates/',views.estimate, name='estimates'),
    path('appinfo/',views.appinfo, name='appinfo'),
    path('customerlist/',views.customerlist,name='customerlist'),
    path('addcustomer/', views.addingcustomer, name='addcustomer'),
    path('deletecustomer/<utility_name>',views.deletecust,name='deletecustomer'),
    path('update/<int:id>', views.updaterecord, name='updaterecord'),
    path('bulkupload/', views.bulk_upload, name='bulkupload'),
    path('uploadlist/', views.uploadlis, name='uploadlist'),
    path('add-customer-form/', views.add_customer_form, name='addcustomer'),
    path('add-existing-user/', views.add_existing_user, name='add-existing-user'),
    path('add-customer-app/', views.add_customer_app, name='add-customer-app'),
    path('new-customer/', views.addcustomer, name='new-customer'),
    path('update-profile-plan/<str:slug>', views.update_profile_plan, name='update-profile-plan'),
    path('messaging/', views.messaging, name='messaging'),
    path('notify/<slug:profile_slug>/', views.notification, name='notify'),
    path('pendingapprovals/', views.pendingapproval, name='pending-approvals'),
    path('transactions/',views.transactions, name='transactions'),

]