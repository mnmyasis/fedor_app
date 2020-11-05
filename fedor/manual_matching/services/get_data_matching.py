from django.core import serializers
import logging, re, time
from manual_matching.models import *

logger = logging.getLogger(__name__)


def matching_data(number_competitor):
    final_matching = FinalMatching.objects.filter(number_competitor = number_competitor)
    data = serializers.serialize('json', final_matching)
    logger.debug('данные final_matching выгружены')
    return data
