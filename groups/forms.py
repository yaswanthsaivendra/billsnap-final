from django import forms
from .models import *
from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget
from accounts.models import *

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'ex: Basic, Premium, Standard ...', 'class': 'w3-input w3-border w3-round'}),
            'description': forms.Textarea(attrs={'placeholder': 'overview', 'class': 'w3-input w3-border w3-round'}),
        }


class SubscribeForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'w3-input w3-border w3-round'})
    )

class UpdateUserGroupForm(forms.Form):
    choice = [
        (1,1)
    ]

    def __init__(self, appslug=None, *args, **kwargs):
        super(UpdateUserGroupForm, self).__init__(*args, **kwargs)
        plans = Group.objects.filter(app__slug=appslug)
        plans_ = []
        for plan in plans:
            plan_ = (plan.id, plan)
            plans_.append(plan_)
        self.fields['update_to'].choices = plans_

    update_to = forms.ChoiceField(
                    choices=choice, 
                    widget=forms.Select(attrs={'placeholder': 'select plan for user ', 'class': 'w3-input w3-border w3-round'}),
                )