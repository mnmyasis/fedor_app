from django.http import JsonResponse
from django.shortcuts import render
from .services.directory_querys import get_number_competitor_list, load_date_new_sku


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