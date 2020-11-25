from django.http import JsonResponse
from django.shortcuts import render
from .services.directory_querys import get_number_competitor_list
# Create your views here.


def number_competitor_list(request):
    """Получить список клиентских справочников"""
    number_competitors = get_number_competitor_list()
    require = {
        'number_competitors': number_competitors
    }
    return JsonResponse(require)