from datetime import datetime

from .services import group_change
from celery import shared_task

@shared_task
def task_group_changes(*args, **kwargs):
    number_competitor = kwargs.get('number_competitor')
    exclude_list = kwargs.get('exclude_list')
    group_change.change_line(number_competitor, exclude_list)
    return "Group changes complete {}".format(datetime.now().strftime('%d-%m-%Y %H:%M'))
