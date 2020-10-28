from .forms.manual_form import *
from .forms.final_matching_form import *

class MatchingWrite(object):
    def write(self, matching_line):
        pass

    def data_preparations(self, matching_line):
        pass

    def write_db(self, matching_data):
        final_matching_form = FinalMatchingForm(matching_data)
        if final_matching_form.is_valid():
            final_matching_form.save()
            return True
        else:
            return False

class BrandNotFound(MatchingWrite):
    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        self.write_db(matching_data)

    def data_preparations(self, matching_line):
        data = {
            'id_sku_dict': matching_line['id_c'],
            'id_eas_dict': 0,
            'type_binding': 4,
            'name_binding': 'Алгоритм не нашел бренд',
            'user': None,
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingOneToOne(MatchingWrite):
    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        self.write_db(matching_data)

    def data_preparations(self, matching_line):
        data = {
            'id_sku_dict': matching_line['id_c'],
            'id_eas_dict': matching_line['id'],
            'type_binding': 1,
            'name_binding': 'Алгоритм',
            'user': None,
            'number_competitor': matching_line['number_competitor'],
            'old_type_binding': 0
        }
        return data


class MatchingManyToOne(MatchingWrite):
    def write(self, matching_line):
        matching_data = self.data_preparations(matching_line)
        self.write_db(matching_data)

    def data_preparations(self, matching_line):
        data = {
            'id_sku_dict': matching_line['id_c'],  # id клиентского справочника
            'id_eas_dict': matching_line['id'],  # id базового справочника
            'lvl': matching_line['num_leven'],
            'lvl2': matching_line['num_fv'],
            'perc_num': matching_line['num_prc'],
            'name_eas': matching_line['tn_fv_prod'],
            'name_sku': matching_line['name'],
            'number_competitor': matching_line['number_competitor'],
        }
        return data

    def write_db(self, matching_data):
        manual_matching_form = ManualMatchingForm(matching_data)
        if manual_matching_form.is_valid():
            manual_matching_form.save()
            return True
        else:
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
        else:
            """Смэтчено один к многим"""
            self.current_state = MatchingManyToOne()

    def wr_match(self, matching_line=None, matching_state=None):
        """Установка статуса мэтчинга алгоритма"""
        self.matching_state = matching_state
        """Получение статуса"""
        self.get_state()
        """Запись в бд"""
        self.current_state.write(matching_line)


if __name__ == '__main__':
    match = Matching()
    [match.wr_match(matching_state=x) for x in range(3)]
