import json
from admin_panel.services import fedor_log
from django.http import JsonResponse
from django.shortcuts import render
from .services.directory_querys import get_number_competitor_list, load_date_new_sku
from .services import group_change
from auth_fedor.views import fedor_permit, fedor_auth_for_ajax
from .tasks import task_group_changes
from admin_panel.models import Tasks


# Create your views here.

@fedor_auth_for_ajax
def number_competitor_list(request):
    """Получить список клиентских справочников"""

    number_competitors = get_number_competitor_list(request.user)
    require = {
        'number_competitors': number_competitors
    }
    return JsonResponse(require)


@fedor_auth_for_ajax
def get_new_sku(request):
    """Дата загрузки номенклатуры в справочнике"""
    number_competitor = json.loads(request.GET.get('number_competitor_id'))
    date_create_new_sku = load_date_new_sku(number_competitor)
    require = {
        'date_create_new_sku': date_create_new_sku
    }
    return JsonResponse(require)


@fedor_permit([1, 2])
def group_change_start(request):
    """Запуск массовых подмен по справочнику"""
    user = request.user
    number_competitor = json.loads(request.GET.get('number_competitor_id'))
    exclude_list = json.loads(request.GET.get('exclude_list'))
    task = task_group_changes.delay(number_competitor=number_competitor, exclude_list=exclude_list)
    Tasks.objects.create(
        task_id=task.id,
        name='Массовые подмены',
        user=request.user,
        status=task.status
    )
    fedor_log.log(
        user=user,
        message='Пользователь({}) - запуск подмен - исключения({}) - id задачи({})'
                ' - справочник({})'.format(user, exclude_list, task.id, number_competitor),
        action=3  # 3 - подмены
    )
    # group_change.change_line(number_competitor, exclude_list)
    return JsonResponse(True, safe=False)


@fedor_permit([1, 2, 3])
def group_changes_list(request):
    """Поиск подмен для их исключения"""
    group_changes_input = request.GET.get('group_changes_input')
    res = group_change.get_group_changes(group_changes_input)
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


@fedor_permit([1, 2, 3])
def group_changes_edit_list(request):
    """Список всех подмен в модальном окне"""
    res = group_change.get_group_changes_list()
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


@fedor_permit([1, 2, 3])
def group_changes_filter(request):
    """Фильтрация подмен в модальном окне"""
    change = request.GET.get('group_change_input')
    search = request.GET.get('group_search_input')
    res = group_change.filter_group_changes(change=change, search=search)
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


@fedor_permit([1, 2, 3])
def group_change_update(request):
    """Изменение записи подмен"""
    user = request.user
    request = json.loads(request.body.decode('utf-8'))
    group_pk = request['data']['pk']
    change = request['data']['change']
    search = request['data']['search']
    require = group_change.update_or_create_group_change(pk=group_pk, change=change, search=search)
    fedor_log.log(
        user=user,
        message='Пользователь({}) - изменение подмены - изменить({}) - найти({}) - id({})'.format(user, change, search, group_pk),
        action=3  # 3 - подмены
    )
    return JsonResponse(require)


@fedor_permit([1, 2, 3])
def group_change_add(request):
    """Добавление подмены в БД"""
    user = request.user
    request = json.loads(request.body.decode('utf-8'))
    change = request['data']['change']
    search = request['data']['search']
    require = group_change.update_or_create_group_change(change=change, search=search)
    fedor_log.log(
        user=user,
        message='Пользователь({}) - добавление подмены - изменить({}) - найти({})'.format(user, change, search),
        action=3  # 3 - подмены
    )
    return JsonResponse(require)
