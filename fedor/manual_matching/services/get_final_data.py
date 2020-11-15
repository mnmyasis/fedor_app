from django.core import serializers
import logging, re, time, json
from manual_matching.models import *
from .get_manual_data import binding_decorator

logger = logging.getLogger(__name__)


@binding_decorator(FinalMatching)
def final_matching_lines(number_competitor, user_id):
    final_matching = FinalMatching.objects.filter(number_competitor=number_competitor, user=user_id).values(
        'eas_dict__pk',
        'eas_dict__tn_fv',
        'sku_dict__name',
        'sku_dict__pk',
        'type_binding',
        'name_binding',
        'number_competitor'
    )
    data = json.dumps(list(final_matching))
    logger.debug('данные final_matching выгружены')
    return data


def final_get_sku(number_competitor, sku_id):
    final_matching = FinalMatching.objects.filter(number_competitor=number_competitor, sku_dict__pk=sku_id).values(
        'eas_dict__pk',
        'eas_dict__tn_fv',
        'sku_dict__name',
        'sku_dict__pk',
        'type_binding',
        'name_binding',
        'number_competitor'
    )
    data = json.dumps(list(final_matching))
    logger.debug('данные final_matching выгружены')
    return data
