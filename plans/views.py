from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from datetime import date
from .forms import *


def subscribe(request, slug, billing_slug):
    if not request.user.is_authenticated:
        return redirect('login')
    plan = Plan.objects.get(slug=slug)
    profile = Profile.objects.get(user=request.user)
    profile.plans.add(plan)
    profile.plan_active = True
    profile.save(update_fields=['plans', 'plan_active'])
    # Creating transaction historh
    create_history(user=request.user, to_plan=plan)
    return redirect('index')

def upgrade_to(request, slug, billing_slug):
    if not request.user.is_authenticated:
        return redirect('login')
    current_plan = Profile.objects.get(user=request.user).plan
    upgrading_to = Plan.objects.get(slug=slug)
    create_history(user=request.user, to_plan=upgrading_to, from_plan=current_plan, upgrade=True)
    profile = Profile.objects.get(user=request.user)
    profile.plans.add(upgrading_to)
    profile.plan_active = True
    profile.save(update_fields=['plans', 'plan_active'])

    return redirect('accountsettings', billing_slug=billing_slug, slug=request.user.username)


def plans_panel(request, slug, billing_slug):
    if request.user.is_superuser:
        if request.method == 'GET':
            plans = Plan.objects.filter(app__slug=slug)
            form = PlanForm()
            payload = {
                'plans': plans,
                'form': form,
                'slug': slug,
                'billing_slug':billing_slug
            }
            return render(request, 'plans-panel/panel.html', payload)
        
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.app = applists.objects.get(slug=slug)
            plan.save()
            return redirect('plans-panel', billing_slug, slug)
        print(form.errors)
        return redirect('plans-panel', billing_slug, slug)
    return redirect('index')

def delete_plan(request, slug, planslug, billing_slug):
    plan = Plan.objects.get(slug__iexact=planslug)
    app = applists.objects.get(slug=slug)
    default_plan = Plan.objects.filter(app=app).filter(default_for_customer=True).first()
    for user in Profile.objects.filter(plans=plan):
        #create_history(user=user.user, to_plan=plan, from_plan=user.plan, upgrade=True)
        user.plans.add(default_plan)
        user.plan_active = True
        user.save(update_fields=['plans', 'plan_active'])
    plan.delete()
    return redirect('plans-panel', billing_slug, slug)

def show_plan(request, slug, billing_slug, planslug):
    if request.user.is_superuser:
        if request.method == 'GET':
            plan = Plan.objects.filter(slug=planslug).first()
            users = Profile.objects.filter(plans=plan)
            form = SubscribeForm()
            userprofile = Profile.objects.filter(user=request.user).first()
            current_plan = userprofile.plans.filter(app = plan.app).first()
            print(current_plan)

            existing_users = Profile.objects.filter(apps=plan.app).exclude(plans=plan)
            payload = {
                'plan': plan,
                'users': users,
                'form': form,
                'update_form': UpdateUserPlanForm(appslug=slug),
                'slug': slug,
                'existing_users' : existing_users,
                'current_plan' : current_plan,
                'billing_slug' : billing_slug
            }
            return render(request, 'plans-panel/plan.html', payload)
        
        # 'POST' method
        form = SubscribeForm(request.POST)
        plan = Plan.objects.filter(slug=planslug).first()
        if form.is_valid():
            #if form.cleaned_data.get("username")!='username':
            customer = Profile.objects.filter(user__username=form.cleaned_data.get("username")).filter(apps__in=[plan.app])
            if customer.exists():
                customer = customer.first()
                pre_plan = customer.plans.filter(app=plan.app).first()
                customer.plans.remove(pre_plan)
                #create_history(user=customer.user, to_plan=plan, from_plan=customer.plan, upgrade=True)
                customer.plans.add(plan)
                customer.plan_active = True
                customer.save(update_fields=['plans', 'plan_active'])
            return redirect('plan', billing_slug, slug, planslug)

            """students = Profile.objects.filter(institute_name=form.cleaned_data.get("institution"), is_student=True)
            for student in students:
                if student.plan==plan:
                    pass
                create_history(user=student.user, to_plan=plan, from_plan=student.plan, upgrade=True)
                student.plan = plan
                student.save(update_fields=['plan'])
            return redirect('plan', slug)"""
        print(forms.error)
        return redirect('plan', billing_slug, slug)


def update_user_plan(request, billing_slug, profileslug,planslug):
    profile = Profile.objects.get(slug__iexact=profileslug)
    current_plan = Plan.objects.get(slug__iexact=planslug)

    form = UpdateUserPlanForm(request.POST)
    new_plan = Plan.objects.get(id=request.POST.get('update_to'))
    profile.plans.remove(current_plan)
    profile.plans.add(new_plan)
    profile.plan_active = True
    profile.save(update_fields=['plans', 'plan_active'])
    return redirect('plans-panel', billing_slug, current_plan.app.slug)
    """if form.is_valid():
        new_plan = Plan.objects.create(
            title=form.cleaned_data.get("title"),
            price=form.cleaned_data.get("price"),
            description=current_plan.description,
            duration=current_plan.duration,
            is_dummy=True
        )
        create_history(user=profile.user, to_plan=new_plan, from_plan=current_plan, upgrade=True)"""
        

# def add_to_plan(request, profileslug, planslug, appslug):
#     userprofile = Profile.objects.filter(slug=profileslug).first()
#     app_plans = Plan.objects.filter()
#     upgrade_to_plan = Plan.objects.filter(slug=planslug).first()
    



