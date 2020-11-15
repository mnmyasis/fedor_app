from .filters import Filter
from manual_matching.models import *
import logging, json

logger = logging.getLogger(__name__)


class FilterStatuses:

    def get_filter_fields(self, fields):
        filter_field = {  # Данные поля будут присутствовать всегда
            'number_competitor': fields['number_competitor'],  # id SKU справочника
        }

        #  Смотрим какие поля пришли с форм поиска на фронте
        if fields['barcode']:
            filter_field['sku_dict__nnt'] = fields['barcode']  # Штриход
        if fields['manufacturer']:
            filter_field['eas_dict__manufacturer__icontains'] = fields['manufacturer']  # Производитель
        if fields['tn_fv']:
            filter_field['eas_dict__tn_fv__icontains'] = fields['tn_fv']  # Наименование номенклатуры
        return filter_field

    def start(self, **fields):
        pass
