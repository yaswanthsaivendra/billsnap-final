from django.urls import path, include
from . import views


urlpatterns = [
    path('addbillingapp/', views.addbillingapp, name='addbillingapp'),
    path('addnonbillingapp/', views.addnonbillingapp, name='addnonbillingapp'),
    path('editapp/<str:aslug>/<int:billing_slug>/', views.editapp, name='editapp'),
    path('all/', views.showapps, name='showapps'),
    path('deleteapp/<aslug>',views.deleteapp,name='deleteapp'),
    path('remove-customer/<str:slug>/<str:userslug>/<int:billing_slug>/',views.remove_user,name='remove-customer'),
    path('<int:billing_slug>/<slug>/', include('dashboard.urls')),
]