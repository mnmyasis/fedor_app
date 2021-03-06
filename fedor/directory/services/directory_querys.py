from directory.models import SyncSKU, Competitors, SyncEAS
from manual_matching.services.get_manual_data import color_line
import json
from datetime import datetime


def get_sku(number_competitor, new_sku=None, barcode_match=False):
    """Тест выгрузка СКУ записей"""
    if new_sku:
        result = SyncSKU.objects.filter(number_competitor__in=number_competitor, matching_status=False,
                                        create_date=new_sku)[:60000]
    else:
        result = SyncSKU.objects.filter(number_competitor__in=number_competitor, matching_status=False)[:60000]
    return result


def get_eas(action):
    """Выгрузка ЕАС для алгоритма"""
    if action:  # по акции
        eas = SyncEAS.objects.filter(status=3)
    else:
        eas = SyncEAS.objects.all()
    return eas


def change_matching_status_sku(sku):
    """Измнения статуса мэтчинга записей СКУ"""
    SyncSKU.objects.filter(pk__in=[x.id for x in sku]).update(matching_status=True)
    return True


def search_by_tn_fv(**fields):
    """Поиск в окне ремэтчинга по ЕАС"""
    filter_fields = {}
    if fields['tn_fv']:
        filter_fields['tn_fv__icontains'] = fields['tn_fv']
    if fields['manufacturer']:
        filter_fields['manufacturer__icontains'] = fields['manufacturer']
    eas = SyncEAS.objects.filter(**filter_fields)[:50].values('pk', 'tn_fv', 'manufacturer')
    eas = color_line(lines=eas, dict_key='tn_fv')
    mfcr = SyncEAS.objects.filter(**filter_fields).distinct('manufacturer')[:12].values('manufacturer')
    eas = json.dumps(list(eas))
    mfcr = json.dumps(list(mfcr))
    res = {
        'res': eas,
        'mfcr': mfcr
    }
    return res


def get_number_competitor_list(user):
    """Список клиентских справочников"""
    if user.profile.access_level.level == 4:  # Если это аптека, выгружаем только её справочник
        number_competitors = Competitors.objects.filter(pk=user.profile.competitor.pk).values('pk', 'name')
    else:
        number_competitors = Competitors.objects.all().values('pk', 'name')
    number_competitors = json.dumps(list(number_competitors))
    return number_competitors


def __my_date_converter(_date):
    """Смена типа date в string"""
    _date = datetime.strftime(_date, '%Y-%m-%d')
    return _date


def load_date_new_sku(number_competitor):
    """Выгрузка даты новых СКУ"""
    date_create_new_sku = SyncSKU.objects.filter(number_competitor__in=number_competitor, matching_status=False) \
        .order_by('create_date').distinct('create_date').values('create_date')
    res = json.dumps(list(date_create_new_sku), default=__my_date_converter)
    return res
