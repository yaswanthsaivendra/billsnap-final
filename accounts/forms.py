import unicodedata
from django.shortcuts import render,redirect

from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

UserModel = get_user_model()


def _unicode_ci_compare(s1, s2):
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def send_mail(self,subject_template_name,email_template_name, context, from_email, to_email, html_email_template_name=None,):

        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u for u in active_users if u.has_usable_password() and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self, domain_override=None, subject_template_name="password_reset_subject.txt", email_template_name="password_reset_email.html", use_https=False, token_generator=default_token_generator, from_email=None, request=None, html_email_template_name=None, extra_email_context=None,
    ):

        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            messages.warning(request, "This mail doesnot exist in our database")
        else:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            email_field_name = UserModel.get_email_field_name()
            for user in self.get_users(email):
                user_email = getattr(user, email_field_name)
                context = {
                    "email": user_email,
                    "domain": domain,
                    "site_name": site_name,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": token_generator.make_token(user),
                    "protocol": "https" if use_https else "http",
                    **(extra_email_context or {}),
                }
                self.send_mail(
                    subject_template_name,
                    email_template_name,
                    context,
                    from_email,
                    user_email,
                    html_email_template_name=html_email_template_name,
                )

from .models import *
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'xp', 'techsnap_cash')

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('image', 'body')
        widgets = {
            'image': forms.FileInput(attrs={'placeholder': 'ex: Basic, Premium, Standard ...', 'class': 'w3-input w3-border w3-round'}),
            'body': forms.Textarea(attrs={'placeholder': 'enter price for the plan', 'class': 'w3-input w3-border w3-round'}),
        }