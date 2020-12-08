import json

from django.http import JsonResponse
from django.shortcuts import render
from .services.directory_querys import get_number_competitor_list, load_date_new_sku
from .services import group_change


# Create your views here.


def number_competitor_list(request):
    """Получить список клиентских справочников"""
    number_competitors = get_number_competitor_list()
    require = {
        'number_competitors': number_competitors
    }
    return JsonResponse(require)


def get_new_sku(request):
    """Дата загрузки номенклатуры в справочнике"""
    number_competitor = request.GET.get('number_competitor_id')
    date_create_new_sku = load_date_new_sku(number_competitor)
    require = {
        'date_create_new_sku': date_create_new_sku
    }
    return JsonResponse(require)


def group_change(request):
    number_competitor = request.GET.get('number_competitor_id')
    exclude_list = json.loads(request.GET.get('exclude_list'))
    group_change.change_line(number_competitor, exclude_list)
    return JsonResponse(True, safe=False)


def group_changes_list(request):
    group_changes_input = request.GET.get('group_changes_input')
    res = group_change.get_group_changes(group_changes_input)
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


def group_changes_edit_list(request):
    res = group_change.get_group_changes_list()
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


def group_changes_filter(request):
    change = request.GET.get('group_change_input')
    search = request.GET.get('group_search_input')
    res = group_change.filter_group_changes(change=change, search=search)
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)


def group_change_update(request):
    request = json.loads(request.body.decode('utf-8'))
    group_pk = request['data']['pk']
    change = request['data']['change']
    search = request['data']['search']
    group_change.update_group_change(pk=group_pk, change=change, search=search)
    return JsonResponse(True, safe=False)
