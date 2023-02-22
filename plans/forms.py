from django import forms
from .models import *
from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget
from accounts.models import *

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ('title', 'price', 'description', 'duration', 'default_for_customer')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex: Basic, Premium, Standard ...', 'class': 'w3-input w3-border w3-round'}),
            'price': forms.NumberInput(attrs={'placeholder': 'enter price for the plan', 'class': 'w3-input w3-border w3-round'}),
            'description': forms.Textarea(attrs={'placeholder': 'overview', 'class': 'w3-input w3-border w3-round'}),
            'duration': forms.Select(attrs={'placeholder': 'duration of plan', 'class': 'w3-input w3-border w3-round'}),
            'default_for_customer': forms.CheckboxInput(attrs={'placeholder': 'Default for every customer', 'class': 'w3-margin w3-check'}),
        }

class SubscribeForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'w3-input w3-border w3-round'}),
    )

class UpdateUserPlanForm(forms.Form):
    choice = [
        (1,1)
    ]

    def __init__(self, appslug=None, *args, **kwargs):
        super(UpdateUserPlanForm, self).__init__(*args, **kwargs)
        plans = Plan.objects.filter(app__slug=appslug)
        plans_ = []
        for plan in plans:
            plan_ = (plan.id, plan)
            plans_.append(plan_)
        self.fields['update_to'].choices = plans_

    update_to = forms.ChoiceField(
                    choices=choice, 
                    widget=forms.Select(attrs={'placeholder': 'select plan for user ', 'class': 'w3-input w3-border w3-round'}),
                )