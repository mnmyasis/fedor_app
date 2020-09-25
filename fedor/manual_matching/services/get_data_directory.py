from auto_matching.models import *
from django.core import serializers
import logging, re, time


logger = logging.getLogger(__name__)

def colorize_text(data):
    logger.debug(data)
    result = []
    for line in data:
        print(line.name)
        ss = re.findall(r'', line.name)

def get_sku_data(number_competitor):
    logger.debug('выгружаются данные ску')
    sku = ClientDirectory.objects.filter(number_competitor = number_competitor)[:30]
    colorize_text(sku)
    data = serializers.serialize('json', sku)

    logger.debug('данные ску выгружены')
    return data
