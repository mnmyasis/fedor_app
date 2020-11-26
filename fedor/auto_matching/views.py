from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import logging, json

from .services.zalivv import *
from .services.client_directory_manipulate import *
from .services.algoritm import *
from .services.write_mathing_result import *
from directory.services.directory_querys import change_matching_status_sku, get_number_competitor_list, test_get_sku

logger = logging.getLogger(__name__)

## @defgroup auto_matching Модуль автоматической стыковки
# @brief Основной модуль, содержащий в себе модули авто-стыковки

## @defgroup auto_matching_interface Интерфейс auto_matching
#  @ingroup auto_matching
#  @param SHOW_AUTO_JOINT_PAGE_TEMPLATE - Глобальные переменная шаблона

## @defgroup show_matching_page Рендер страницы
#  @ingroup auto_matching_interface

SHOW_AUTO_MATCHING_PAGE_TEMPLATE = 'auto_matching/auto_matching_page.html'


## @ingroup show_matching_page
# @{
# @login_required(login_url='/auth/login/')
@ensure_csrf_cookie
def auto_matching_page(request):
    """Рендер страницы авто-стыковки"""
    logger.info(request.session.get('style_interface'))
    return render(request, SHOW_AUTO_MATCHING_PAGE_TEMPLATE, {})


##@}


## @defgroup search_client Поиск по ClientDirectory
#  @ingroup auto_joint_interface

## @ingroup search_client
# @{
def search_client_directory_data(request):
    """Поиск по клиентскому справочнику, форма поиска на интерфейсе"""
    logger.debug('Запуск поиска по ClientDirectory')
    logger.debug(request)
    search_client_data = request.GET.get('search_client_data')
    number_competitor_id = request.GET.get('number_competitor_id')

    logger.debug('Поисковой запрос: {}'.format(search_client_data))
    client_data = search_client_directory(search_client_data, number_competitor_id)
    result = {'client_data': client_data}
    return JsonResponse(result)


##@}


def algoritm_mathing(request):
    """Функция запуска алгоритма"""
    request = json.loads(request.body.decode('utf-8'))
    number_competitor_id = request['data']['number_competitor_id']
    """Получаем список записей СКУ"""
    sku_data = test_get_sku(number_competitor_id)  # Выгрузка из справочника directory/services/sku_querys
    """Запускаем алгоритм"""
    ts = Test()
    matching_result = ts.get_match_result(sku_data)
    change_matching_status_sku(sku_data)  # Изменение поля matching_status directory/services/sku_querys
    match = Matching()
    [match.wr_match(matching_state=x['qnt'], matching_line=x) for x in matching_result['data']]
    return JsonResponse(True, safe=False)


def inject_base_directory(request):
    zalivchik()


def inject_client_directory(request):
    zaliv_client_dict()
