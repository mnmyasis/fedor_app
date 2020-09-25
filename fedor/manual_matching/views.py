from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from .services.get_data_directory import *
import logging

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
