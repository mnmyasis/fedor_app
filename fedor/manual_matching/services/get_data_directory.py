from directory.models import *
from manual_matching.models import *
from django.core import serializers
import logging, re, time


logger = logging.getLogger(__name__)



def get_sku_data(number_competitor):
    logger.debug('выгружаются данные ску')
    sku = ManualMatchingData.objects.filter(number_competitor = number_competitor).distinct('id_sku_dict')[:30]
    data = serializers.serialize('json', sku)
    logger.debug('данные ску выгружены')
    return data

def get_eas_data(sku_id):
    logger.debug('выгружаются данные eas')
    eas = ManualMatchingData.objects.filter(id_sku_dict=sku_id)
    data = serializers.serialize('json', eas)
    logger.debug('данные eas выгружены')
    return data
