from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from .services.get_data_directory import *
import logging, json

logger = logging.getLogger(__name__)

## @defgroup manual_matching Модуль ручного мэтчинга

## @defgroup manual_matching Интерфейс manual_matching
#  @ingroup manual_matching
#  @param SHOW_MANUAL_MATCHING_PAGE_TEMPLATE - Глобальные переменная шаблона

## @defgroup show_manual_matching_page Рендер страницы
#  @ingroup manual_matching

SHOW_MANUAL_MATCHING_PAGE_TEMPLATE = 'manual_matching/manual_matching_page.html'


## @ingroup show_manual_matching_page
# @{
def show_manual_matching_page(request):
    return render(request, SHOW_MANUAL_MATCHING_PAGE_TEMPLATE)
##@}

def get_sku(request):
    """Получить записи из SKU"""
    number_competitor = request.GET.get('number_competitor_id')
    logger.debug(number_competitor)
    sku = get_sku_data(number_competitor)
    result = {'sku': sku}
    return JsonResponse(result)

def get_eas(request):
    """Получить записи из ЕАС"""
    sku_id = request.GET.get('sku_id')
    logger.debug(sku_id)
    eas = get_eas_data(sku_id)
    result = {'eas': eas}
    return JsonResponse(result)

def match_eas_sku(request):
    """Смэтчить СКУ к ЕАС вручную"""
    request = json.loads(request.body.decode('utf-8'))
    sku_id = request['data']['sku_id']
    eas_id = request['data']['eas_id']
    logger.debug('sku_id: {} ----> eas_id: {}'.format(sku_id, eas_id))
    return JsonResponse(True, safe=False)


