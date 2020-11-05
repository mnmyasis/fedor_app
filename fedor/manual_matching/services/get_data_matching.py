from django.core import serializers
import logging, re, time, json
from manual_matching.models import *

logger = logging.getLogger(__name__)


def matching_data(number_competitor):
    final_matching = FinalMatching.objects.filter(number_competitor = number_competitor).values(
        'eas_dict__pk',
        'eas_dict__tn_fv',
        'sku_dict__name',
        'sku_dict__pk',
        'type_binding',
        'name_binding',
        'number_competitor'
    )
    #data = serializers.serialize('json', final_matching)
    data = json.dumps(list(final_matching))
    logger.debug('данные final_matching выгружены')
    return data
