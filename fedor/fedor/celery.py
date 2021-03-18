import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fedor.settings')
celery_app = Celery('fedor')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'reset-sku-user-binding': {
        'task': 'admin_panel.tasks.reset_sku_binding',
        'schedule': crontab(hour=4, minute=00),
    },
    'eas_sync': {
        'task': 'admin_panel.tasks.eas_api',
        'schedule': crontab(hour=14, minute=39),
    },
}

'''celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}'''
