from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import logging, json

from .services.zalivv import *
from .services.client_directory_manipulate import *

logger = logging.getLogger(__name__)

## @defgroup auto_joint Модуль автоматической стыковки
# @brief Основной модуль, содержащий в себе модули авто-стыковки

## @defgroup auto_joint_interface Интерфейс auto_joint
#  @ingroup auto_joint
#  @param SHOW_AUTO_JOINT_PAGE_TEMPLATE - Глобальные переменная шаблона

## @defgroup show_joint_page Рендер страницы
#  @ingroup auto_joint_interface

SHOW_AUTO_JOINT_PAGE_TEMPLATE = 'auto_joint/auto_joint_page.html'


## @ingroup show_joint_page
# @{
#@login_required(login_url='/auth/login/')
@ensure_csrf_cookie
def show_auto_joint_page(request):
    """Рендер страницы авто-стыковки"""
    logger.info(request.session.get('style_interface'))
    return render(request, SHOW_AUTO_JOINT_PAGE_TEMPLATE, {})
##@}


## @defgroup search_client Поиск по ClientDirectory
#  @ingroup auto_joint_interface

## @ingroup search_client
# @{
def search_client_directory_data(request):
    """Поиск по клиентскому справочнику, форма поиска на интерфейсе"""
    logger.debug('Запуск поиска по ClientDirectory')
    search_client_data = request.GET.get('search_client_data')
    number_competitor_id = request.GET.get('number_competitor_id')

    logger.debug('Поисковой запрос: {}'.format(search_client_data))
    client_data = search_client_directory(search_client_data, number_competitor_id)
    result = {'client_data': client_data}
    return JsonResponse(result)


##@}

def joint_element(request):
    """Выборочная стыковка"""
    request = json.loads(request.body.decode('utf-8'))
    logger.debug(request)
    id_client_directory = request['data']['id_client_directory']
    number_competitor_id = request['data']['number_competitor_id']
    logger.debug('id_client_dict: {}'.format(id_client_directory))
    return JsonResponse(True, safe=False)


def inject_base_directory(request):
    zalivchik()


def inject_client_directory(request):
    zaliv_client_dict()
