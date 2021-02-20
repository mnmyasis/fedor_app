from directory.models import *
from manual_matching.models import *
from django.core import serializers
import logging, re, time, json

logger = logging.getLogger(__name__)


def binding_decorator(model):
    """Декоратор привязки записей к пользователю"""

    def wrapper(func):
        def wrap_binding(*args, **kwargs):
            count_data = model.objects.filter(
                number_competitor=kwargs['number_competitor'],
                user=kwargs['user_id']).distinct('sku_dict').count()  # Кол-во записей привязанных к пользователю
            logger.debug('Id пользователя - {}    Записей - {}'.format(kwargs['user_id'], count_data))
            if count_data < 10:  # Если записей у пользователя меньше 10, привязывается еще 50шт.
                model.objects.filter(pk__in=
                                     model.objects.filter(number_competitor=kwargs['number_competitor'],
                                                          user=None).distinct(
                                         'sku_dict').values('pk')[:50]
                                     ).update(user=kwargs['user_id'])  # Привязка данных к юзеру
            return func(*args, **kwargs)

        return wrap_binding

    return wrapper


def color_line(lines, dict_key):
    skus = []
    for line in lines:
        tmp_lines = re.split(' ', line[dict_key])
        end_line = '<strong style="color: red;">{}</strong>'.format(tmp_lines[0])
        i = 1
        while i < len(tmp_lines):
            end_line = end_line + ' {}'.format(tmp_lines[i])
            i += 1
        line[dict_key] = end_line
        skus.append(line)
    return skus


@binding_decorator(ManualMatchingData)
def get_sku_data(number_competitor, user_id):
    logger.debug('выгружаются данные ску --- справочник {}'.format(number_competitor))
    sku = ManualMatchingData.objects.filter(
        number_competitor=number_competitor,
        matching_status=False,
        user=user_id).distinct('sku_dict__pk').values(
            'sku_dict',
            'name_sku'
        )
    sku = color_line(lines=sku, dict_key='name_sku')
    data = json.dumps(list(sku))
    logger.debug('данные ску выгружены -- {}'.format(len(sku)))
    return data


def get_eas_data(sku_id):
    logger.debug('выгружаются данные eas')
    eas = ManualMatchingData.objects.filter(sku_dict__pk=sku_id).values(
        'eas_dict',
        'name_eas'
    )
    eas = color_line(lines=eas, dict_key='name_eas')
    print(eas)
    data = json.dumps(list(eas))
    logger.debug('данные eas выгружены -- {}'.format(len(eas)))
    return data
