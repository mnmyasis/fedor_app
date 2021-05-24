from celery import shared_task
from datetime import datetime
from directory.services.directory_querys import change_matching_status_sku, get_sku, get_eas
from auto_matching.services.write_mathing_result import Matching
from auto_matching.services import algoritm
from django.contrib.sessions.models import Session
from manual_matching.models import ManualMatchingData
from api.services.sync_directory import request_eas_api, request_sku_api


class SKUException(Exception):
    pass


class EASException(Exception):
    pass


@shared_task
def create_task_starting_algoritm(*args, **kwargs):
    """Запуск алгоритма"""
    number_competitor_id = kwargs['number_competitor_id']
    action = kwargs.get('action')
    barcode_match = kwargs.get('barcode_match')
    new_sku = kwargs.get('new_sku')
    """"Список записей СКУ"""
    sku_data = get_sku(number_competitor_id, new_sku)  # Выгрузка из справочника directory/services/sku_querys
    if len(sku_data) == 0:  # Пустой клиентский справочник
        raise SKUException("No entries sku")
    eas_dict = get_eas(action)
    if len(eas_dict) == 0:  # Пустой базовый справочник
        raise EASException("No entries eas")
    alg = algoritm.Matching()
    """Запуск мэтчинга по щтрихкоду"""
    barcode_match_result, sku = alg.barcode_matching(sku_data, number_competitor_id, eas_dict, barcode_match)
    """Запуск алгоритм"""
    if len(sku) > 0:  # Если все записи смэтчились по штрихкоду
        matching_result = alg.start_test(sku, eas_dict)  # Старт алгоритма
    change_matching_status_sku(sku_data)  # Изменение поля matching_status directory/services/sku_querys
    """Запись результата работы алгоритма"""
    match = Matching()
    [match.wr_match(matching_state=x['qnt'], matching_line=x) for x in
     barcode_match_result]  # Запись мэчтинга по штрихкоду
    if len(sku) > 0:  # Если все записи смэтчились по штрихкоду
        [match.wr_match(matching_state=x['qnt'], matching_line=x) for x in
         matching_result['data']]  # Запись мэчтинга алгоритма
    return 'Matching complete {}!'.format(datetime.now().strftime('%d-%m-%Y %H:%M'))


@shared_task
def reset_sku_binding():
    """Сброс привязанных данных к пользователю"""
    Session.objects.all().delete()
    ManualMatchingData.objects.exclude(user=None).update(user=None)
    return 'Access reset sku binding user'


@shared_task
def eas_api():
    """Сбор данных ЕАС"""
    start = datetime.now()
    res = request_eas_api()
    end = datetime.now()
    result_time = end - start
    return 'eas sync: {}'.format(result_time)


@shared_task
def sku_api():
    """Сбор данных СКУ"""
    start = datetime.now()
    res = request_sku_api()
    end = datetime.now()
    result_time = end - start
    return 'sku sync: {}'.format(result_time)
