from manual_matching.models import *
from auto_matching.services.write_mathing_result import Matching
from directory.models import SyncSKU
import logging

logger = logging.getLogger(__name__)


def matching_sku_eas(sku_id, eas_id, number_competitor, user_id, type_binding):
    logger.debug("Match sku_id - {} eas_id - {} competitor - {}".format(sku_id, eas_id, number_competitor))
    matching = Matching()
    match_line = {
        'id_sku': sku_id,
        'id_eas': eas_id,
        'number_competitor': number_competitor,
        'user': user_id,
        'type_binding': type_binding
    }
    res = matching.wr_match(matching_state='manual', matching_line=match_line)  # Запись в final_matching
    if res:
        logger.debug('Успешно записано в final')
        """Удаление смэтченных записей"""
        ManualMatchingData.objects.filter(sku_dict__pk=sku_id, number_competitor=number_competitor).delete()
        return True
    else:
        logger.debug('СКУ успешно ремэтчинулось ску:{} еас:{}'.format(sku_id, eas_id))
        return True


def delete_matching(sku_id, competitor):
    match = FinalMatching.objects.get(sku_dict__pk=sku_id, number_competitor=competitor)
    sku = SyncSKU.objects.get(pk=match.sku_dict.pk)
    sku.matching_status = True
    sku.save()
    match.delete()
    return True

