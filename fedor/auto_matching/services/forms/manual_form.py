from django import forms
from manual_matching.models import *


class ManualMatchingForm(forms.ModelForm):
    class Meta:
        model = ManualMatchingData
        fields = '__all__'

