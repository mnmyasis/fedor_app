from directory.models import ClientDirectory, BaseDirectory
import json


def test_get_sku(number_competitor):
    result = ClientDirectory.objects.filter(number_competitor=number_competitor, matching_status=False)[:30]
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
