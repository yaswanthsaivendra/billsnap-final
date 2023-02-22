from django.urls import path
from accounts import views as acc_views
from django.contrib.auth import views as a_views

app_name='accounts'

urlpatterns = [
    path('register/', acc_views.RegistrationView.as_view(), name='register'),

    path('register/<str:appslug>/<int:billing_slug>/', acc_views.app_registration, name='register-app'),
    
    path('login/', acc_views.LoginView.as_view(), name='login'),
    path('logout/', acc_views.logout, name='logout'),
    path('activate/<uidb64>/<token>', acc_views.VerificationView.as_view(), name='activate'),
    path('reset_password/', acc_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset-password'),
    path('reset_password_sent/', a_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', a_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password-reset-confirm'),
    path('reset_password_complete/', a_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password-reset-complete'),
    path('<str:slug>/edit/<str:userslug>/<int:billing_slug>/', acc_views.update_profile, name='update-profile'),
    path('<str:slug>/<str:userslug>/<int:billing_slug>/', acc_views.ShowProfile.as_view(), name='show-profile'),
    path('<str:slug>/<str:userslug>/<str:planslug>/<int:billing_slug>/', acc_views.update_plan, name='update-plan'),

    path('create-notification/<str:slug>/<int:billing_slug>/', acc_views.create_notification, name='create-notification'),
]