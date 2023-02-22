from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib import auth, messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from apps.models import *

from logging.handlers import TimedRotatingFileHandler
import logging
logger=logging.getLogger()
logging.basicConfig(
        handlers=[ TimedRotatingFileHandler('logs.log', when="midnight", interval=1)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')


def app_registration(request, appslug, billing_slug):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    context = {
        'username': username,
        'email': email,
        'slug': appslug
    }
    if not User.objects.filter(username=username).exists():
        if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, 'Password is too short')
                return render(request, 'register.html')

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()

            profile = Profile.objects.get(user=user)
            profile.apps.add(applists.objects.get(slug=appslug))
            messages.success(
                request, 'Account successfully created! Check your Email for Account Activation')
            return redirect('addcustomer', slug=appslug, billing_slug=billing_slug)

        messages.warning(request, "This Email already exists!")
        return render(request, 'register.html', context)
    else:
        messages.warning(request, "This username already exists!")
        return render(request, 'register.html', context)

class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'username': username,
            'email': email,
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'register.html')

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('accounts:activate', kwargs={
                            'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject="Activate your Account"
                activate_url = 'http://'+domain+link
                email_body = 'Hi, ' + user.username + \
                    ' Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'from@example.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(
                    request, 'Account successfully created! Check your Email for Account Activation')
                return redirect('accounts:login')

            messages.warning(request, "This Email already exists!")
            return render(request, 'register.html', context)
        else:
            messages.warning(request, "This username already exists!")
            return render(request, 'register.html', context)

from django.utils.encoding import force_str

class VerificationView(View):
    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            auth.login(request, user,
                    backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return render(request, 'login.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if 'login_page' in request.POST:
            next = request.POST.get('next')
            username = request.POST['username']
            password = request.POST['password']
            context = {
                'user_found': True,
                'user_name': username
            }
            if username and password:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(
                        username=username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            is_customer=Profile.objects.get(user=user).admin
                            if is_customer:
                                messages.success(request,"loggedin succesfully")
                                return redirect("showapps")
                            else:
                                messages.success(request,"loggedin succesfully")
                                return redirect("index")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )

                elif User.objects.filter(email=username).exists():
                    user = User.objects.get(email=username)
                    user = auth.authenticate(
                        username=user.username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            is_admin=Profile.objects.get(user=user).admin
                            if is_admin:
                                messages.success(request,"loggedin succesfully")
                                return redirect("showapps")
                            else:
                                messages.success(request,"loggedin succesfully")
                                return redirect("custdash")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )
                elif (User.objects.filter(email=username).exists() or User.objects.filter(username=username).exists() == False):
                    messages.warning(
                        request, "The username or Email you have entered does not exist.")
                    return render(request, 'login.html', context)

            context = {
                'user_found': True,
                'user_name': username
            }
            messages.warning(request, 'Invalid credentials, try again')
            return render(request, 'login.html', context)

        return render(request, "login.html")

def logout(request):
    logger.info(request.user.username+"_ logged out")
    auth.logout(request)
    return redirect('index')

from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .utils import token_generator

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

from .forms import PasswordResetForm

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

from decimal import Context
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, auth
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from plans.forms import UpdateUserPlanForm
from .models import Profile
from .forms import ProfileForm
from dashboard.forms import *
from .forms import *

# Create your views here.
def update_profile(request, slug, userslug, billing_slug):
    profile = get_object_or_404(Profile, slug=userslug)
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        status = request.POST.get('status')

        utility_name = request.POST.get('utility_name')
        utility_short_name = request.POST.get('utility_short_name')
        utility_state= request.POST.get('utility_state')
        utility_district = request.POST.get('utility_district')
        utility_country = request.POST.get('utility_country')
        utility_postalcode = request.POST.get('utility_postalcode')
        utility_address = request.POST.get('utility_address')
        
        contact_person = request.POST.get('contact_person')
        contact_email = request.POST.get('contact_email')
        contact_phnum = request.POST.get('contact_phnum')
        contact_mobile= request.POST.get('contact_mobile')
        contact_designation= request.POST.get('contact_designation')
        contact_landline= request.POST.get('contact_landline')

        emergency_person= request.POST.get('emergency_person')
        emergency_altperson= request.POST.get('emergency_altperson')
        emergency_mobile= request.POST.get('emergency_mobile')
        emergency_altmobile= request.POST.get('emergency_altmobile')
        emergency_officeaddress= request.POST.get('emergency_officeaddress')
        emergency_altofficeaddress= request.POST.get('emergency_altofficeaddress')


        profile.full_name = full_name
        profile.status = status
        profile.utility_name = utility_name
        profile.utility_short_name = utility_short_name
        profile.utility_state = utility_state
        profile.utility_district = utility_district
        profile.utility_country = utility_country
        profile.utility_postalcode = utility_postalcode
        profile.utility_address = utility_address
        profile.contact_person = contact_person
        profile.contact_email = contact_email
        profile.contact_phnum = contact_phnum
        profile.contact_mobile = contact_mobile
        profile.contact_designation = contact_designation
        profile.contact_landline = contact_landline
        profile.emergency_person = emergency_person
        profile.emergency_altperson = emergency_altperson
        profile.emergency_mobile = emergency_mobile
        profile.emergency_altmobile = emergency_altmobile
        profile.emergency_officeaddress = emergency_officeaddress
        profile.emergency_altofficeaddress = emergency_altofficeaddress


        profile.save()
        logger.info(request.user.username+"_ updated profile")
        messages.success(request, "Profile has been updated")

        return HttpResponseRedirect(reverse('accounts:show-profile', kwargs={'slug':slug ,'userslug':userslug, 'billing_slug':billing_slug}))

# class UpdateProfile(UpdateView):
#     model = Profile
#     template_name = 'editprofile.html'
#     form_class = ProfileForm
#     success_url = '/'

class ShowProfile(DetailView):
    model = Profile
    template_name = 'myprofile.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Profile,slug = self.kwargs['userslug'])

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfile, self).get_context_data(*args, **kwargs)
        page_profile = get_object_or_404(Profile, slug=self.kwargs['userslug'])
        print(page_profile)
        context['profile'] = page_profile
        context['updateform'] = UpdateUserPlanForm(appslug=self.kwargs['slug'])
        context['plan'] = page_profile.plans.filter(app__slug=self.kwargs['slug']).first()
        print(context['plan'])
        context['notification_form'] = NotificationForm()
        context['slug'] = self.kwargs['slug']
        context['userslug'] = self.kwargs['userslug']
        app = applists.objects.filter(slug=self.kwargs['slug']).first()
        plans = Plan.objects.filter(app=app)
        context['plans'] = plans
        context['billing_slug'] = self.kwargs['billing_slug']
        if self.request.user==page_profile.user:
            self.template_name = 'myprofile.html'
        elif self.request.user!=page_profile.user or self.request.user.is_anonymous:
            self.template_name = 'myprofile.html'
        return context

def create_notification(request, slug, billing_slug):
    if request.method=='POST':
        profile = Profile.objects.get(user=request.user)
        form = NotificationForm(request.POST, request.FILES)
        if form.is_valid():
            url = 'https://url.com/some-url/'
            notification = form.save(commit=False)
            notification.profile = profile
            notification.url = url
            notification.save(update_fields=['profile', 'url'])
            return redirect('accounts:show-profile', userslug=profile.slug, slug=slug, billing_slug=billing_slug)
        print(form.errors)
        return redirect('accounts:show-profile', userslug=profile.slug, slug=slug, billing_slug=billing_slug)

def update_plan(request, slug, userslug ,planslug, billing_slug):
    profile = Profile.objects.get(slug__iexact=userslug)
    current_plan = Plan.objects.get(slug__iexact=planslug)

    form = UpdateUserPlanForm(request.POST)
    new_plan = Plan.objects.get(id=request.POST.get('update_to'))
    profile.plans.remove(current_plan)
    profile.plans.add(new_plan)
    profile.plan_active = True
    profile.save(update_fields=['plans', 'plan_active'])
    messages.success(request, "Plan has been successfully updated")
    return redirect('accounts:show-profile', slug=slug, userslug=userslug, billing_slug=billing_slug)