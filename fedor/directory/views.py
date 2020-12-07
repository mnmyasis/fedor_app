import json

from django.http import JsonResponse
from django.shortcuts import render
from .services.directory_querys import get_number_competitor_list, load_date_new_sku
from .services.group_change import change_line, get_group_changes


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
    change_line(number_competitor, exclude_list)
    return JsonResponse(True, safe=False)


def group_changes_list(request):
    group_changes_input = request.GET.get('group_changes_input')
    res = get_group_changes(group_changes_input)
    require = {
        'group_changes_list': res
    }
    return JsonResponse(require)

