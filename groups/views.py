from django.shortcuts import render, redirect
from accounts.models import *
from .models import *
from datetime import date
from django.http import JsonResponse
from .forms import *

# Create your views here.


def groups_panel(request, slug, billing_slug):
    if request.user.is_superuser:
        if request.method == 'GET':
            groups = Group.objects.filter(app__slug=slug)
            plans = Plan.objects.filter(app__slug = slug)
            form = GroupForm()
            payload = {
                'groups': groups,
                'form': form,
                'slug': slug,
                'plans' : plans,
                'billing_slug':billing_slug
            }
            return render(request, 'groups-panel/panel.html',payload)
        
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.app = applists.objects.get(slug=slug)
            group.save()
            return redirect('groups:groups-panel', billing_slug, slug)
        print(form.errors)
        return redirect('groups-panel', billing_slug, slug)
    return redirect('index')

def delete_group(request, slug, appslug, billing_slug):
    group = Group.objects.get(slug__iexact=slug)
    group.delete()
    return redirect('groups:groups-panel', billing_slug, appslug)

def show_group(request, slug, groupslug, billing_slug):
    if request.user.is_superuser:
        if request.method == 'GET':
            group = Group.objects.filter(slug=groupslug).first()
            users = group.members.all()
            form = SubscribeForm()
            existing_users = Profile.objects.filter(apps=group.app).exclude(group=group)
            payload = {
                'group': group,
                'users': users,
                'form': form,
                'update_form': UpdateUserGroupForm(appslug=group.app.slug),
                'slug': slug,
                'existing_users': existing_users,
                'billing_slug' : billing_slug
            }
            return render(request, 'groups-panel/group.html', payload)
        
        # 'POST' method
        form = SubscribeForm(request.POST)
        group = Group.objects.filter(slug=groupslug).first()
        if form.is_valid():
            #if form.cleaned_data.get("username")!='username':
            customer = Profile.objects.filter(user__username=form.cleaned_data.get("username")).filter(apps__in=[group.app])
            if customer.exists():
                customer = customer.first()
                # pre_group = customer.group_set.filter(app__appname=group.app.appname).first()
                # if pre_group:
                #     pre_group.members.remove(customer)
                #create_history(user=customer.user, to_group=group, from_group=customer.group, upgrade=True)
                group.members.add(customer)
            return redirect('groups:group', billing_slug, slug)

            """students = Profile.objects.filter(institute_name=form.cleaned_data.get("institution"), is_student=True)
            for student in students:
                if student.group==group:
                    pass
                create_history(user=student.user, to_group=group, from_group=student.group, upgrade=True)
                student.group = group
                student.save(update_fields=['group'])
            return redirect('group', slug)"""
        print(forms.error)
        return redirect('group', billing_slug, slug)

def add_customer_to_group(request, groupslug, billing_slug):
    username = request.GET.get('username')
    user = Profile.objects.get(user__username=username)

    group = Group.objects.get(slug=groupslug)
    
    # pre_group = user.group_set.filter(app__appname=group.app.appname).first()
    # if pre_group:
    #     pre_group.members.remove(user)

    group.members.add(user)
    return JsonResponse({})

def remove_customer_from_group(request, groupslug, billing_slug):
    username = request.GET.get('username')
    user = Profile.objects.get(user__username=username)

    group = Group.objects.get(slug=groupslug)

    group.members.remove(user)
    return JsonResponse({})



# def update_user_group(request, slug, groupslug):
#     profile = Profile.objects.get(slug__iexact=slug)

#     current_group = Group.objects.get(slug=groupslug)
#     new_group = Group.objects.get(id=request.POST.get('update_to'))

#     current_group.members.remove(profile)
#     new_group.members.add(profile)

#     return redirect('groups:groups-panel', current_group.app.slug)
    """if form.is_valid():
        new_group = group.objects.create(
            title=form.cleaned_data.get("title"),
            price=form.cleaned_data.get("price"),
            description=current_group.description,
            duration=current_group.duration,
            is_dummy=True
        )
        create_history(user=profile.user, to_group=new_group, from_group=current_group, upgrade=True)"""
        

def show_plan_group(request, slug, plangroupslug, billing_slug):
    if request.user.is_superuser:
        if request.method == 'GET':
            plan = Plan.objects.filter(slug=plangroupslug).first()
            users = Profile.objects.filter(plans=plan)
                    
            payload = {
                'plan': plan,
                'users': users,
                'slug' : slug,
                'billing_slug' : billing_slug
            }
            return render(request, 'groups-panel/plangroup.html', payload)