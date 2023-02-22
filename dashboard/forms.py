from dataclasses import fields
from django import forms
from .models import customer
from plans.models import *

class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = [ 'utility_name' ,'utility_short_name' ,'utility_state' ,'utility_district' ,'utility_country' ,'utility_postalcode' ,'utility_address' ,'contact_person' ,'contact_email' ,'contact_phnum' ,'contact_mobile' ,'contact_designation' ,'contact_landline' ,'emergency_person' ,'emergency_altperson' ,'emergency_mobile' ,'emergency_altmobile' ,'emergency_officeaddress' ,'emergency_altofficeaddress']
    
class UpdateProfilePlanForm(forms.Form):
    choice = [(1,1)]
    def __init__(self, appslug=None, profile=None, *args, **kwargs):
        super(UpdateProfilePlanForm, self).__init__(*args, **kwargs)
        plans = Plan.objects.filter(app__slug=appslug)
        plans_ = []
        for plan in plans:
            plan_ = (plan.id, plan)
            plans_.append(plan_)
        self.fields['update_to'].choices = plans_
        self.fields['paid'].initial = profile.paid
        self.fields['plan_active'].initial = profile.plan_active

    paid = forms.BooleanField(
        initial=False, 
        required=False,
        widget=forms.CheckboxInput(attrs={'placeholder': 'Default for every customer', 'class': 'w3-margin w3-check'}),
    )
    plan_active = forms.BooleanField(
        initial=False, 
        required=False,
        widget=forms.CheckboxInput(attrs={'placeholder': 'Default for every customer', 'class': 'w3-margin w3-check'}),
    )
    update_to = forms.ChoiceField(
        choices=choice, 
        widget=forms.Select(attrs={'placeholder': 'select plan for user ', 'class': 'w3-input w3-border w3-round'}),
    )