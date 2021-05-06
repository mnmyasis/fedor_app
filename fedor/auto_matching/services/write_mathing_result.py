from .forms.manual_form import *
from .forms.final_matching_form import *
import logging

logger = logging.getLogger(__name__)


class MatchingWrite(object):
    def write(self, matching_line):
        pass

    def data_preparations(self, matching_line):
        pass

    def write_db(self, matching_data):
        final_matching_form = FinalMatchingForm(matching_data)
        if final_matching_form.is_valid():
            res = final_matching_form.save()
            return res
        else:
            return False


class BrandNotFound(MatchingWrite):
    """Запись в финальную таблицу, алгоритм не нашел вариантов мэтчинга"""

    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        self.write_db(matching_data)

    def data_preparations(self, matching_line):
        data = {
            'sku_dict': matching_line['id_c'],
            'eas_dict': 0,
            'type_binding': 4,
            'name_binding': 'Не найдено соответствие в ЕАС',
            'user': None,
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingOneToOne(MatchingWrite):
    """Алгоритм смэтчил один к одному, запись в финальную таблицу"""

    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        res = self.write_db(matching_data)
        return res

    def data_preparations(self, matching_line):
        data = {
            'sku_dict': matching_line['id_c'],
            'eas_dict': matching_line['id'],
            'type_binding': 8,
            'name_binding': 'Алгоритм',
            'user': None,
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingBarcode(MatchingWrite):
    """Мэтчинг по штрихкоду, запись в финальную таблицу"""

    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        res = self.write_db(matching_data)
        return res

    def data_preparations(self, matching_line):
        data = {
            'sku_dict': matching_line['id_c'],
            'eas_dict': matching_line['id'],
            'type_binding': 2,
            'name_binding': 'Мэтчинг по ШК - проверка не требуется',
            'user': None,
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingManual(MatchingWrite):
    """Запись в финальную таблицу ручного мэтчинга пользователем"""

    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)  # Подготовка данных к записи
        res = self.write_db(matching_data)  # Запись в бд
        return res

    def data_preparations(self, matching_line):
        """Подготовка данных к записи"""
        type_binding = 0
        name_binding = ''
        id_sku = matching_line['id_sku']
        id_eas = matching_line['id_eas']
        if matching_line['type_binding'] == 3:
            type_binding = 3
            name_binding = 'Мэтчинг вручную'
        if matching_line['type_binding'] == 5:
            type_binding = 5
            name_binding = 'Предложено к добавлению в ЕАС'
            id_eas = None
        if matching_line['type_binding'] == 6:
            type_binding = 6
            name_binding = 'Прочее'
            id_eas = None
        data = {
            'sku_dict': id_sku,
            'eas_dict': id_eas,
            'type_binding': type_binding,
            'name_binding': name_binding,
            'user': matching_line['user'],
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingManyToOne(MatchingWrite):
    """Запись данных на ручной мэтчинг"""

    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)  # Подготовка данных к записи
        res = self.write_db(matching_data)  # Запись в бд
        return res

    def data_preparations(self, matching_line):
        """Подготовка данных к записи"""
        data = {
            'sku_dict': matching_line['id_c'],  # id клиентского справочника
            'eas_dict': matching_line['id'],  # id базового справочника
            'lvl': matching_line['num_leven'],
            'lvl2': matching_line['num_fv'],
            'perc_num': matching_line['num_prc'],
            'name_eas': matching_line['tn_fv_prod'],
            'name_sku': matching_line['name'],
            'number_competitor': matching_line['number_competitor'],
        }
        return data

    def write_db(self, matching_data):
        """Запись в бд"""
        logger.debug(matching_data)
        manual_matching_form = ManualMatchingForm(matching_data)
        if manual_matching_form.is_valid():
            logger.debug('Смэтчено один к многим')
            res = manual_matching_form.save()
            return res
        else:
            logger.debug('Смэтчено один к многим не прошел валидность')
            return False


class Matching(object):
    def __init__(self):
        self.current_state = None
        self.matching_state = None

    def get_state(self):
        if self.matching_state is None:
            return False
        if self.matching_state == 0:
            """Алгоритм не нашел брэнд"""
            self.current_state = BrandNotFound()
        elif self.matching_state == 1:
            """Смэтчено один к одному"""
            self.current_state = MatchingOneToOne()
        elif self.matching_state == 'manual':
            """Смэтчено вручную"""
            self.current_state = MatchingManual()
        elif self.matching_state == 'barcode_true':
            """Мэтчинг по ШК - проверка не требуется"""
            self.current_state = MatchingBarcode()
        elif self.matching_state == 'barcode_false':
            """Мэтчинг по ШК - требуется проверка"""
            self.current_state = MatchingManyToOne()
        else:
            """Смэтчено один к многим"""
            self.current_state = MatchingManyToOne()

    def wr_match(self, matching_line=None, matching_state=None):
        """Установка статуса мэтчинга алгоритма"""
        self.matching_state = matching_state
        """Получение статуса"""
        self.get_state()
        """Запись в бд"""
        res = self.current_state.write(matching_line)
        return res


if __name__ == '__main__':
    match = Matching()
    [match.wr_match(matching_state=x) for x in range(3)]
