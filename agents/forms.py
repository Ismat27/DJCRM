from django import forms
from django.forms import Select
from leads.models import Agent

class AgentModelForm(forms.ModelForm):

    class Meta:
        model = Agent
        fields = (
            'user',
        )

        widgets = {
             'user': Select(attrs={
                'class': 'form-select mt-3',
                
            }),
        }