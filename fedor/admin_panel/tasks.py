from celery import shared_task
from datetime import datetime
from directory.services.directory_querys import get_sku, change_matching_status_sku
from auto_matching.services.write_mathing_result import Matching
from auto_matching.services import algoritm
from django.contrib.sessions.models import Session
from manual_matching.models import ManualMatchingData
from admin_panel.services.sync_directory import request_eas_api, request_sku_api


@shared_task
def create_task_starting_algoritm(*args, **kwargs):
    number_competitor_id = kwargs['number_competitor_id']
    action = kwargs.get('action')
    barcode_match = kwargs.get('barcode_match')
    new_sku = kwargs.get('new_sku')
    """Получаем список записей СКУ"""
    sku_data = get_sku(number_competitor_id)  # Выгрузка из справочника directory/services/sku_querys
    """Запускаем алгоритм"""
    alg = algoritm.Matching()
    matching_result = alg.start(sku_data)
    change_matching_status_sku(sku_data)  # Изменение поля matching_status directory/services/sku_querys
    """Запись результата работы алгоритма"""
    match = Matching()
    [match.wr_match(matching_state=x['qnt'], matching_line=x) for x in matching_result['data']]
    return 'Matching complete {}!'.format(datetime.now().strftime('%d-%m-%Y %H:%M'))


@shared_task
def reset_sku_binding():
    Session.objects.all().delete()
    ManualMatchingData.objects.exclude(user=None).update(user=None)
    return 'Access reset sku binding user'


@shared_task
def eas_api():
    start = datetime.now()
    res = request_eas_api()
    end = datetime.now()
    result_time = end - start
    return 'eas sync: {}'.format(result_time)

@shared_task
def sku_api():
    start = datetime.now()
    res = request_sku_api()
    end = datetime.now()
    result_time = end - start
    return 'sku sync: {}'.format(result_time)

@shared_task
def sync_directory(api_func):
    start = datetime.now()
    res = api_func()
    end = datetime.now()
    result_time = end - start
    return 'directory sync: {}'.format(result_time)




