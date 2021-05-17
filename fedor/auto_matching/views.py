from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from admin_panel.services import fedor_log
import logging, json
from .services.zalivv import *
from .services import algoritm
from .services.write_mathing_result import *
from directory.services.directory_querys import change_matching_status_sku, get_number_competitor_list, test_get_sku, \
    test_new_sku, get_eas
from auth_fedor.views import fedor_permit, fedor_auth_for_ajax
from admin_panel.tasks import create_task_starting_algoritm
from admin_panel.models import Tasks

logger = logging.getLogger(__name__)

SHOW_AUTO_MATCHING_PAGE_TEMPLATE = 'auto_matching/auto_matching_page.html'


@fedor_permit([1, 2, 3])
def auto_matching_page(request):
    """Рендер страницы авто-мэтчинга"""
    return render(request, SHOW_AUTO_MATCHING_PAGE_TEMPLATE, {})


@fedor_permit([1, 2])
def algoritm_mathing(request):
    """Функция запуска алгоритма DEV"""
    user = request.user
    request = json.loads(request.body.decode('utf-8'))
    number_competitor_id = json.loads(request['data']['number_competitor_id'])
    action = request['data']['action']  # Акция
    barcode_match = request['data']['barcode_match']  # Доверять ШК
    new_sku = request['data']['new_sku']  # Новая ску номенклатура
    """Список записей СКУ"""
    sku_data = test_get_sku(number_competitor_id, new_sku)  # Выгрузка из справочника directory/services/sku_querys
    if len(sku_data) == 0:
        result = {
            'error': False,
            'error_message': None,
            'access': "Справочник Товаров клиентов пуст"
        }
        return JsonResponse(result)
    eas_dict = get_eas(action)
    if len(eas_dict) == 0:
        result = {
            'error': False,
            'error_message': None,
            'access': "Справочник ЕАС пуст"
        }
        return JsonResponse(result)
    alg = algoritm.Matching()
    """Запуск мэтчинга по щтрихкоду"""
    barcode_match_result, sku = alg.barcode_matching(sku_data, number_competitor_id, eas_dict, barcode_match)
    """Запускаем алгоритм"""
    matching_result = alg.start_test(sku, eas_dict)
    #change_matching_status_sku(sku_data)  # Изменение поля matching_status directory/services/sku_querys
    """Запись результата работы алгоритма"""
    fedor_log.log(
        user=user,
        message='Пользователь({}) - запуск алгоритма - справочник({}) - акция({}) - довреять ШК({}) - новая '
                'номенклатура({})'.format(user, number_competitor_id, action, barcode_match, new_sku),
        action=2  # 2 - запуск алгоритма
    )
    #match = Matching()
    #[match.wr_match(matching_state=x['qnt'], matching_line=x) for x in barcode_match_result]  # Запись мэчтинга по штрихкоду
    #[match.wr_match(matching_state=x['qnt'], matching_line=x) for x in matching_result['data']]  # Запись мэчтинга алгоритма
    return JsonResponse(True, safe=False)


@fedor_permit([1, 2])
def create_work_algoritm(request):
    """Функция создания задачи алгоритма"""
    user = request.user
    request = json.loads(request.body.decode('utf-8'))
    number_competitor_id = json.loads(request['data'].get('number_competitor_id'))
    action = request['data'].get('action')  # Акция
    barcode_match = request['data'].get('barcode_match')  # Доверять ШК
    new_sku = request['data'].get('new_sku')  # Новая ску номенклатура
    task = create_task_starting_algoritm.delay(
        number_competitor_id=number_competitor_id,
        action=action,
        barcode_match=barcode_match,
        new_sku=new_sku
    )
    fedor_log.log(
        user=user,
        message='Пользователь({}) - запуск алгоритма - справочник({}) - акция({}) - довреять ШК({}) - новая '
                'номенклатура({}) - id задачи({})'.format(user, number_competitor_id, action, barcode_match, new_sku, task.id),
        action=2  # 2 - запуск алгоритма
    )
    Tasks.objects.create(
        task_id=task.id,
        name='Алгоритм',
        user=user,
        status=task.status
    )
    return JsonResponse(True, safe=False)


def inject_base_directory(request):
    zalivchik()


def inject_client_directory(request):
    zaliv_client_dict()


def injects_group_change(request):
    group_change()
