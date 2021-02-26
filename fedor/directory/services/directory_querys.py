from directory.models import ClientDirectory, BaseDirectory, NumberCompetitor
import json
from django.core import serializers
from datetime import datetime


def test_get_sku(number_competitor):
    result = ClientDirectory.objects.filter(number_competitor=number_competitor, matching_status=False)[:100]
    return result


def change_matching_status_sku(sku):
    ClientDirectory.objects.filter(pk__in=[x.id for x in sku]).update(matching_status=True)
    return True


def search_by_tn_fv(**fields):
    filter_fields = {}
    if fields['tn_fv']:
        filter_fields['tn_fv__icontains'] = fields['tn_fv']
    elif fields['manufacturer']:
        filter_fields['manufacturer__icontains'] = fields['manufacturer']
    else:
        return False
    res = BaseDirectory.objects.filter(**filter_fields)[:50].values('pk', 'tn_fv', 'manufacturer')
    res = json.dumps(list(res))
    return res


def get_number_competitor_list(user):
    if user.profile.access_level.level == 4:
        number_competitors = NumberCompetitor.objects.filter(pk=user.profile.competitor.pk).values('pk', 'name')
    else:
        number_competitors = NumberCompetitor.objects.all().values('pk', 'name')
    number_competitors = json.dumps(list(number_competitors))
    return number_competitors


def __my_date_converter(_date):
    """Смена типа date в string"""
    _date = datetime.strftime(_date, '%Y-%m-%d')
    return _date


def load_date_new_sku(number_competitor):
    date_create_new_sku = ClientDirectory.objects.filter(number_competitor=number_competitor, matching_status=False) \
        .order_by('create_date').distinct('create_date').values('create_date')
    res = json.dumps(list(date_create_new_sku), default=__my_date_converter)
    return res
