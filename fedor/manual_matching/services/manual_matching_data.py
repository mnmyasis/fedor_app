from manual_matching.models import *
from directory.models import *
from auto_matching.services.write_mathing_result import Matching
from analytic.services import statistic
import logging

logger = logging.getLogger(__name__)


def matching_sku_eas(sku_id, eas_id, number_competitor, user_id):
    logger.debug("Match sku_id - {} eas_id - {} competitor - {}".format(sku_id, eas_id, number_competitor))
    matching = Matching()
    match_line = {
        'id_sku': sku_id,
        'id_eas': eas_id,
        'number_competitor': number_competitor,
        'user': user_id
    }
    res = matching.wr_match(matching_state='manual', matching_line=match_line)
    logger.debug(res)
    if res:
        statistic.statistic_write(
            user_id=user_id,
            sku_id=sku_id,
            eas_id=eas_id,
            number_competitor=number_competitor,
            action=1
        )
        logger.debug('Успешно записано в final')
        """Удаление смэтченных записей"""
        ManualMatchingData.objects.filter(sku_dict__pk=sku_id, number_competitor=number_competitor).delete()
        return True
    else:
        statistic.statistic_write(
            user_id=user_id,
            sku_id=sku_id,
            eas_id=eas_id,
            number_competitor=number_competitor,
            action=2
        )
        logger.debug('СКУ успешно ремэтчинулось ску:{} еас:{}'.format(sku_id, eas_id))
        return True


def edit_status(sku_id, number_competitor, type_binding, user_id):
    logger.debug("Update status sku_id - {}  competitor - {}  status - {}".format(sku_id, number_competitor, type_binding))
    types_binding = [
        {'status': 1, 'binding_name': 'Мэтчинг по ШК - требуется проверка'},
        {'status': 2, 'binding_name': 'Мэтчинг по ШК - проверка не требуется'},
        {'status': 3, 'binding_name': 'Мэтчинг вручную'},
        {'status': 4, 'binding_name': 'Не найдено соответствие в ЕАС'},
        {'status': 5, 'binding_name': 'Предложено к добавлению в ЕАС'},
        {'status': 6, 'binding_name': 'Прочее'},
        {'status': 7, 'binding_name': 'Смэтчено аптекой'},
    ]
    for type_bind in types_binding:
        print(sku_id)
        if type_bind['status'] == int(type_binding):
            FinalMatching.objects.filter(
                sku_dict__pk=sku_id,
                number_competitor=number_competitor).update(
                type_binding=type_binding,
                name_binding=type_bind['binding_name']
            )

            statistic.statistic_write(
                user_id=user_id,
                sku_id=sku_id,
                eas_id=FinalMatching.objects.get(sku_dict__pk=sku_id).eas_dict.pk,
                number_competitor=number_competitor,
                action=3
            )
