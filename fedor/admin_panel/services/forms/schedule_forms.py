from django import forms
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class CrontabScheduleForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = ('minute', 'hour', 'day_of_week', 'month_of_year')
