from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from .services.get_data_directory import *
from .services.get_data_matching import *
from .services.manual_matching_data import *
from .services.filters import *
import logging, json

logger = logging.getLogger(__name__)

## @defgroup manual_matching Модуль ручного мэтчинга

## @defgroup manual_matching Интерфейс manual_matching
#  @ingroup manual_matching
#  @param SHOW_MANUAL_MATCHING_PAGE_TEMPLATE - Глобальные переменная шаблона

## @defgroup show_manual_matching_page Рендер страницы
#  @ingroup manual_matching

SHOW_MANUAL_MATCHING_PAGE_TEMPLATE = 'manual_matching/page.html'


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
    match = matching_sku_eas(sku_id, eas_id)
    if match:
        number_competitor = request['data']['number_competitor_id']
        sku = get_sku_data(number_competitor)
        result = {'sku': sku}
        return JsonResponse(result)
    else:
        return JsonResponse(False, safe=False, status=500)


def get_final_matching(request):
    number_competitor = request.GET.get('number_competitor_id')
    logger.debug(number_competitor)
    data = final_matching_lines(number_competitor)
    result = {'matching': data}
    return JsonResponse(result)


def edit_match(request):
    """изменить статус мэтчинга"""
    request = json.loads(request.body.decode('utf-8'))
    number_competitor = request['data']['number_competitor_id']
    sku_id = request['data']['sku_id']
    type_binding = request['data']['type_binding']
    edit_status(
        sku_id=sku_id,
        number_competitor=number_competitor,
        type_binding=type_binding
    )

    data = final_get_sku(number_competitor=number_competitor, sku_id=sku_id)
    result = {'matching': data}
    return JsonResponse(result)


def filter_matching(request):
    number_competitor = request.GET.get('number_competitor_id')  # Справочник СКУ
    sku_id = request.GET.get('sku_id')  # ID номенклатуры СКУ
    manufacturer = request.GET.get('manufacturer')  # Производитель
    tn_fv = request.GET.get('tn_fv')  # Строка номенклатуры ЕАС

    filter_match = Filter(FilterManufacturer())
    data = filter_match.business_logic(
        sku_id=sku_id,
        number_competitor=number_competitor,
        manufacturer=manufacturer,
        tn_fv=tn_fv
    )
    result = {'eas': data}
    return JsonResponse(result)
