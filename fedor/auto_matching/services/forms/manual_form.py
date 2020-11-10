from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max
from manual_matching.models import *
from directory.models import ClientDirectory


class ManualMatchingForm(forms.ModelForm):
    class Meta:
        model = ManualMatchingData
        fields = '__all__'

