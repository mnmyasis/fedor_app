import logging, json
from manual_matching.models import *
logger = logging.getLogger(__name__)


#@binding_decorator(FinalMatching)
def final_matching_lines(number_competitor, user_id, sku_id):
    """Выгрузка результатов мэтчинга в таблицу"""
    final_matching = FinalMatching.objects.filter(user__pk=user_id, number_competitor__in=number_competitor).order_by('-pk').values(
        'eas_dict__pk',
        'eas_dict__tn_fv',
        'sku_dict__name',
        'sku_dict__pk',
        'type_binding',
        'name_binding',
        'number_competitor')
    data = json.dumps(list(final_matching))
    return data
