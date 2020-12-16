from django.http import JsonResponse
from django.shortcuts import render
from .services import statistic
from datetime import datetime
# Create your views here.
ANALYTIC_PAGE = 'analytic/page.html'


def analytic_page(request):
    return render(request, ANALYTIC_PAGE)


def status_matchings(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(start_date)
    print(end_date)
    now = datetime.now()
    require = statistic.status_matchings(start_date=start_date, end_date=end_date, number_competitor=1)
    return JsonResponse(require)