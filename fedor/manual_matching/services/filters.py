from directory.models import *
from django.core import serializers
from manual_matching.models import *
import logging, json

logger = logging.getLogger(__name__)


class Filter:

    def __init__(self, filter_matching):
        self.filter_matching = filter_matching

    def set_filter_matching(self, filter_matching):
        self.filter_matching = filter_matching

    def get_filter_matching(self):
        return self.filter_matching

    def business_logic(self, **fields):
        fm = self.get_filter_matching()
        result = fm.start(**fields)
        try:
            data = serializers.serialize('json', result)
        except AttributeError:
            data = result
        return data


class ManualFilter:

    def get_filter_fields(self, fields):
        filter_field = {  # Данные поля будут присутствовать всегда
            'sku_dict__pk': fields['sku_id'],  # id SKU
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

    def get_manufacturer(self, **filter_field):
        """выгрузка для выпадающего списка фильтра Производитель"""
        manufacturer = ManualMatchingData.objects.filter(**filter_field).values('eas_dict__manufacturer') \
            .distinct('eas_dict__manufacturer')
        manufacturer = json.dumps(list(manufacturer))
        return manufacturer

    def get_tn_fv(self, **filter_field):
        """выгрузка для выпадающего списка фильтра Номенклатура"""
        tn_fv = ManualMatchingData.objects.filter(**filter_field).values('eas_dict__tn_fv').distinct('eas_dict__tn_fv')
        tn_fv = json.dumps(list(tn_fv))
        return tn_fv

    def get_barcode(self, **filter_field):
        """выгрузка для выпадающего списка фильтра Штрихкод"""
        barcode = ManualMatchingData.objects.filter(**filter_field).values('sku_dict__nnt').distinct('sku_dict__nnt')
        barcode = json.dumps(list(barcode))
        return barcode

    def get_eas(self, **filter_field):
        """выгрузка для таблицы SKU"""
        eas = ManualMatchingData.objects.filter(**filter_field).values('eas_dict', 'name_eas')
        eas = json.dumps(list(eas))
        return eas

    def start(self, **fields):
        logger.debug(fields)
        filter_field = self.get_filter_fields(fields)  # Подгон полей для поиска по модели
        eas = self.get_eas(**filter_field)  # Выгрузка данных для таблицы SKU

        if fields['manufacturer']:
            manufacturer = self.get_manufacturer(**filter_field)  # Выгрузка для выпадающего списка в фильтре
            # производитель
        else:
            manufacturer = None
        if fields['tn_fv']:
            tn_fv = self.get_tn_fv(**filter_field)  # Выгрузка для выпадающего списка в фильтре номенклатура
        else:
            tn_fv = None
        if fields['barcode']:
            barcode = self.get_barcode(**filter_field)  # Выгрузка для выпадающего списка в фильтре штрихкод
        else:
            barcode = None
        result = {'eas': eas, "manufacturer": manufacturer, 'tn_fv': tn_fv, 'barcode': barcode}

        return result


class SKUFilter:

    def start(self, **fields):
        sku = ManualMatchingData.objects.filter(**fields).distinct('sku_dict__pk').values('sku_dict__pk', 'name_sku')
        sku = json.dumps(list(sku))
        result = {'sku': sku}
        return result


if __name__ == '__main__':
    filter_match = Filter(FilterManufacturer())
    res = filter_match.business_logic(
        sku_id=666,
        number_competitor=2,
        eas_dict__manufacturer='burugaga',
        eas_dict__tn_fv='zelenka'
    )
    print(res)
