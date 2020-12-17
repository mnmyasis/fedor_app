from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from .services import statistic
from directory.models import NumberCompetitor
import json
# Create your views here.
ANALYTIC_PAGE = 'analytic/page.html'


def analytic_page(request):
    return render(request, ANALYTIC_PAGE)


def status_matchings(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    competitors = NumberCompetitor.objects.all()
    res = []
    for competitor in competitors:
        st = statistic.status_matchings(start_date=start_date, end_date=end_date, number_competitor=competitor.pk)
        res.append({
            'competitor_name': competitor.name,
            'competitor_pk': competitor.pk,
            'values': st
        })
    require = {
        'stats': res
    }
    #require = statistic.status_matchings(start_date=start_date, end_date=end_date, number_competitor=1)
    return JsonResponse(require)