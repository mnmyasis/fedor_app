from celery import shared_task
from datetime import datetime
from directory.services.directory_querys import test_get_sku, change_matching_status_sku
from auto_matching.services.write_mathing_result import Matching
from auto_matching.services.algoritm import Test


@shared_task
def adding_task(x, y):
    time.sleep(10)
    return x + y

@shared_task
def create_task_starting_algoritm(*args, **kwargs):
    number_competitor_id = kwargs['number_competitor_id']
    action = kwargs.get('action')
    barcode_match = kwargs.get('barcode_match')
    new_sku = kwargs.get('new_sku')
    """Получаем список записей СКУ"""
    sku_data = test_get_sku(number_competitor_id)  # Выгрузка из справочника directory/services/sku_querys
    """Запускаем алгоритм"""
    ts = Test()
    matching_result = ts.get_match_result(sku_data)
    change_matching_status_sku(sku_data)  # Изменение поля matching_status directory/services/sku_querys
    """Запись результата работы алгоритма"""
    match = Matching()
    [match.wr_match(matching_state=x['qnt'], matching_line=x) for x in matching_result['data']]
    return 'Matching complete {}!'.format(datetime.now().strftime('%d-%m-%Y %H:%M'))
