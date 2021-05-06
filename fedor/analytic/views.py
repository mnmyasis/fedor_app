from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .services import statistic
from directory.models import Competitors
from auth_fedor.views import fedor_permit, fedor_auth_for_ajax
import json

# Create your views here.
ANALYTIC_PAGE = 'analytic/page.html'


@login_required
@fedor_permit([1, 2, 3])
def analytic_page(request):
    """Страница аналитики"""
    return render(request, ANALYTIC_PAGE)


def status_matchings(request):
    """Накопления по статусам мэтчинга"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    competitors = Competitors.objects.all()
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
    return JsonResponse(require)


def status_changes(request):
    """Виды изменения статусов"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    competitor = json.loads(request.GET.get('number_competitor'))
    competitor = 1
    st = statistic.status_changes(start_date=start_date, end_date=end_date, number_competitor=competitor)
    require = {
        'stats': st
    }
    return JsonResponse(require)


def user_status_changes(request):
    """Измененные статусы пользователем"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    competitor = request.GET.get('number_competitor')
    competitor = 1
    st = statistic.status_user_changes(start_date=start_date, end_date=end_date, number_competitor=competitor)
    require = {
        'stats': st
    }
    return JsonResponse(require)


def user_rating(request):
    """Рейтинг пользователей"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    competitor = request.GET.get('number_competitor')
    competitor = 1
    st = statistic.user_rating(start_date=start_date, end_date=end_date, number_competitor=competitor)
    require = {
        'stats': st
    }
    return JsonResponse(require)


def raw_sku(request):
    """Необработанные"""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    st = statistic.load_raw_sku(start_date=start_date, end_date=end_date)
    require = {
        'stats': st
    }
    return JsonResponse(require)
