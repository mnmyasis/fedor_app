from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from .services.get_manual_data import get_sku_data, get_eas_data
from .services.get_final_data import final_get_sku, final_matching_lines
from .services.manual_matching_data import matching_sku_eas, edit_status
from .services.filters import Filter, ManualFilter, SKUFilter
from .services.filters_final import FilterStatuses
from directory.services.directory_querys import search_by_tn_fv
from auth_fedor.views import fedor_permit, fedor_auth_for_ajax
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

@login_required
def show_manual_matching_page(request):
    logger.debug(request.user.pk)
    return render(request, SHOW_MANUAL_MATCHING_PAGE_TEMPLATE)


##@}

@fedor_auth_for_ajax
def get_sku(request):
    """Получить записи из SKU"""
    logger.debug(request.user.pk)
    user_id = request.user.pk
    number_competitor = request.GET.get('number_competitor_id')
    logger.debug(number_competitor)
    sku = get_sku_data(number_competitor=number_competitor, user_id=user_id)
    result = {'sku': sku}
    return JsonResponse(result)


@fedor_auth_for_ajax
def get_eas(request):
    """Получить записи из ЕАС"""
    sku_id = request.GET.get('sku_id')
    logger.debug(sku_id)
    eas = get_eas_data(sku_id)
    result = {'eas': eas}
    return JsonResponse(result)


@fedor_auth_for_ajax
def match_eas_sku(request):
    """Смэтчить СКУ к ЕАС вручную"""
    user_id = request.user.pk
    request = json.loads(request.body.decode('utf-8'))
    sku_id = request['data']['sku_id']
    eas_id = request['data']['eas_id']
    number_competitor = request['data']['number_competitor_id']
    logger.debug('sku_id: {} ----> eas_id: {}'.format(sku_id, eas_id))
    match = matching_sku_eas(sku_id, eas_id, number_competitor, user_id)  # Мэтчинг в final_matching id записей
    if match:  # Если запись прошла без ошибок, подгружаются еще данные
        sku = get_sku_data(number_competitor=number_competitor, user_id=user_id)
        result = {'sku': sku}
        logger.debug('смэтчено')
        return JsonResponse(result)
    else:
        return JsonResponse(True, safe=False)  # Запись успешно обновлена


@fedor_auth_for_ajax
def get_final_matching(request):
    user_id = request.user.pk
    number_competitor = request.GET.get('number_competitor_id')
    logger.debug(number_competitor)
    data = final_matching_lines(number_competitor=number_competitor, user_id=user_id)
    result = {'matching': data}
    return JsonResponse(result)


@fedor_auth_for_ajax
def edit_match(request):
    """изменить статус мэтчинга"""
    req = json.loads(request.body.decode('utf-8'))
    number_competitor = req['data']['number_competitor_id']
    sku_id = req['data']['sku_id']
    type_binding = req['data']['type_binding']
    edit_status(
        sku_id=sku_id,
        number_competitor=number_competitor,
        type_binding=type_binding,
        user_id=request.user.pk
    )

    data = final_get_sku(number_competitor=number_competitor, sku_id=sku_id)
    result = {'matching': data}
    return JsonResponse(result)


@fedor_auth_for_ajax
def filter_matching(request):
    """Фильтры ручного мэтчинга по таблице ЕАС"""
    number_competitor = request.GET.get('number_competitor_id')  # Справочник СКУ
    sku_id = request.GET.get('sku_id')  # ID номенклатуры СКУ
    manufacturer = request.GET.get('manufacturer')  # Производитель
    tn_fv = request.GET.get('tn_fv')  # Строка номенклатуры ЕАС
    barcode = request.GET.get('barcode')  # ШК НСКЗ

    filter_match = Filter(ManualFilter())
    result = filter_match.business_logic(
        sku_id=sku_id,
        number_competitor=number_competitor,
        manufacturer=manufacturer,
        tn_fv=tn_fv,
        barcode=barcode
    )
    return JsonResponse(result)


@fedor_auth_for_ajax
def filter_for_sku_list(request):
    """Фильтры ручного мэтчинга SKU"""
    type_filter = int(request.GET.get('type_filter'))
    line = request.GET.get('search_line')
    number_competitor = request.GET.get('number_competitor_id')

    user_id = request.user.pk
    search_line = {'user': user_id, 'number_competitor': number_competitor}
    if type_filter == 1:
        search_line['sku_dict__nnt'] = line
    elif type_filter == 2:
        search_line['name_sku__icontains'] = line
    else:
        return JsonResponse(False, safe=False)
    sku_filter = Filter(SKUFilter())
    res = sku_filter.business_logic(**search_line)
    return JsonResponse(res)


@fedor_auth_for_ajax
def filter_statuses(request):
    """Фильтр по статусу мэтчинга"""
    number_competitor = request.GET.get('number_competitor_id')
    statuses = json.loads(request.GET.get('statuses'))
    user_id = request.user.pk
    statuses_filter = Filter(FilterStatuses())
    result = statuses_filter.business_logic(number_competitor=number_competitor, statuses=statuses, user_id=user_id)
    return JsonResponse(result)


@fedor_auth_for_ajax
def re_match_filter(request):
    """Фильтрация по ЕАС tn_fv AND manufacturer"""
    tn_fv = request.GET.get('tn_fv')
    manufacturer = request.GET.get('manufacturer')
    res = search_by_tn_fv(tn_fv=tn_fv, manufacturer=manufacturer)
    result = {'eas': res}
    return JsonResponse(result)
