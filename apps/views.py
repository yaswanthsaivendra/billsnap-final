from django.shortcuts import render, redirect, get_object_or_404
from .models import applists
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from logging.handlers import TimedRotatingFileHandler
from accounts.models import *
import logging
from plans.models import Plan
from groups.models import Group

logger=logging.getLogger()
logging.basicConfig(
        handlers=[ TimedRotatingFileHandler('logs.log', when="midnight", interval=1)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

@login_required
def addbillingapp(request):
    applis= applists()
    plan = Plan()
    group = Group()

    if request.method=='POST':
        app_name = request.POST.get('app_name')
        app_im= request.FILES.get('app_im')

        plan_name = request.POST.get('plan_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        duration = request.POST.get('duration')


        auth=request.user

        applis.appname=app_name
        applis.appimg= app_im
        applis.author= auth
        applis.save()

        plan.title = plan_name
        plan.price = price
        plan.description = description
        plan.duration = duration
        plan.app = applis
        plan.default_for_customer=True
        plan.save()

        logger.info(request.user.username+"_added an billing app")
        return redirect('showapps')
    else:
        return render(request, 'addbillingapp.html')



@login_required
def addnonbillingapp(request):
    applis= applists()

    if request.method=='POST':
        app_name = request.POST.get('app_name')
        app_im= request.FILES.get('app_im')


        auth=request.user

        applis.appname=app_name
        applis.appimg= app_im
        applis.author= auth
        applis.is_billing = False
        applis.save()
        logger.info(request.user.username+"_added an non billing app")
        return redirect('showapps')
    else:
        return render(request, 'addnonbillingapp.html')


from django.contrib import messages
@login_required
def showapps(request):
    billingappli=applists.objects.all()
    leni=len(billingappli)
    mssg="logged in sucessfully"
    logger.info(request.user.username+"_seen the whole applist")
    return render(request,'showapps.html',{'showapp':billingappli,'leni':leni,'msg':mssg})

@login_required
def deleteapp(request,aslug):
    deli=applists.objects.get(slug=aslug)
    deli.delete()
    logger.info(request.user.username+"_deleted an app")
    return redirect('showapps')

def remove_user(request, slug, userslug, billing_slug):
    profile = Profile.objects.get(slug=userslug)
    app = applists.objects.get(slug=slug)
    app_plans = Plan.objects.filter(app=app)
    for plan in app_plans:
        if profile.plans.filter(id=plan.id).exists():
            profile.plans.remove(plan)
    app_groups = Group.objects.filter(app=app)
    for group in app_groups:
        if group.members.filter(id=profile.id).exists():
            group.members.remove(profile)
    profile.apps.remove(app)


    return redirect('customerlist', billing_slug=billing_slug, slug=slug)



@login_required
def editapp(request, aslug, billing_slug):
    app = applists.objects.get(slug=aslug)
    if request.method=='POST':
        app.appimg= request.FILES.get('app_im')
        app.save()
        logger.info(request.user.username+"_edited an app")
        return redirect('appinfo', billing_slug=billing_slug, slug=aslug)
    