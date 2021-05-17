import json
import re
from datetime import datetime
from directory.models import GroupChangeTable, SyncSKU
from django.db.models import BooleanField, Value


def __replace_line(line, change_lines):  # Не забыть удалить эту функцию
    """Изменение записей по шаблону подмен"""
    old_name = line.name
    new_name = ''
    for ch_line in change_lines:
        line.name = re.sub(r'\s(,)\s', ' ', line.name)  # Удаление запятых
        line.name = re.sub(r'(,)\s', ' ', line.name)  # Удаление запятых
        counter_equality = 0  # Счетчик кол-ва совпавших букв нскз с подменой
        string = 0  # Первое совпадение символа ску с подменой
        for x in range(0, len(line.name)):  # Побуквенное сравнивание
            """Здесь должны совпасть подряд все символы подмены с подстрокой ску"""
            if line.name[x] == ch_line.search[counter_equality]:  # Если буква совпала
                if counter_equality == 0: string = x  # Запись id первого совпадения
                if counter_equality <= len(ch_line.search): counter_equality += 1  # Переход на след букву строки подмен
                if counter_equality == len(ch_line.search):  # Счетчик совпавших букв подмены равен длинне строки
                    if len(line.name) == x + 1:  # Конец строки ску
                        if ' ' == line.name[string - 1]:  # Есть ли пробел перед подстрокой ску
                            change = True
                        else:
                            change = False
                    else:
                        if ' ' == line.name[string - 1] and ' ' == line.name[x + 1]:  # Пробел перед/после подстроки ску
                            change = True
                        else:
                            change = False
                    if change:
                        """:string от начала строки до первого совпадения, подмена, x+1:len(line.name) всё после подмены"""
                        new_name = line.name[:string] + ch_line.change + line.name[x + 1: len(line.name)]
                        break
                    else:  # Сброс счетчиков, подстрока является частью другого слова
                        string = 0
                        counter_equality = 0
            else:  # Если буква не совпала сброс счетчиков
                string = 0
                counter_equality = 0
    line.save()
    print('old: {}---->new: {}'.format(old_name, new_name))
    return True


def __replace_line2(line, change_lines):
    """МАССОВЫЕ ПОДМЕНЫ"""
    new_name = ""
    old_name = line.name
    line.name = line.name.upper()  # Перевод строки ску в верхний регистр
    for ch_line in change_lines:
        ch_line.search = ch_line.search.upper()  # Перевод строки подмен search в верхний регистр
        first_equality = line.name.find(ch_line.search)  # Поиск первого совпадения
        if first_equality != -1:  # Если есть совпадение
            ch_line.change = ch_line.change.upper()  # Перевод строки подмен change в верхний регистр
            last_equality = first_equality + len(ch_line.search)  # Нахождение последнего вхождения в строке ску
            max_length = len(line.name)  # Длинна строки
            line.name = line.name[0:first_equality] + ch_line.change + line.name[last_equality:max_length]  # Вставка подмены
            new_name = line.name
            print('old: {}---->new: {}'.format(old_name, new_name))
    line.save()
    print('old: {}---->new: {}'.format(old_name, new_name))


def change_line(number_competitor, exclude_list):
    """Запуск массовых подмен"""
    start = datetime.now()
    names = SyncSKU.objects.filter(number_competitor__in=number_competitor)  # Список записей СКУ
    change_lines = GroupChangeTable.objects.exclude(pk__in=[exclude.get('pk') for exclude in exclude_list]).extra(
        select={'length': 'Length(search)'}).order_by('-length')
    for name in names:
        __replace_line2(name, change_lines)  # Изменение записей СКУ по шаблону подмен
    end = datetime.now()
    result_time = end - start
    return result_time


def get_group_changes(group_changes_input):
    """Выгрузка данных из Массовых подмен"""
    changes_list = GroupChangeTable.objects.filter(search__icontains=group_changes_input)[:10].values('pk', 'search')
    changes_list = json.dumps(list(changes_list))
    return changes_list


def get_group_changes_list():
    """Выгрузка всей таблицы массовых подмен"""
    # changes_list = GroupChangeTable.objects.all().values('pk', 'search', 'change')
    # .annotate(upcoming=Value(True, output_field=BooleanField()))
    changes_list = GroupChangeTable.objects.annotate(exclude=Value(False, output_field=BooleanField())) \
                       .order_by('search')[:100].values('pk', 'search', 'change', 'exclude')
    changes_list = json.dumps(list(changes_list))
    return changes_list


def filter_group_changes(**fields):
    """Фильтр массовых подмен, используется в модальном окне"""
    filter_fields = {}
    if fields['change']:
        filter_fields['change__icontains'] = fields['change']
    if fields['search']:
        filter_fields['search__icontains'] = fields['search']
    gr_changes = GroupChangeTable.objects.filter(**filter_fields).annotate(
        exclude=Value(False, output_field=BooleanField())) \
                     .order_by('search')[:100].values('pk', 'search', 'change', 'exclude')
    gr_changes = json.dumps(list(gr_changes))
    return gr_changes


def update_or_create_group_change(change, search, pk=None):
    """Изменение или добавление массовых подмен, используется в модальном окне"""
    res = {
        'change': change,
        'search': search
    }
    obj, created = GroupChangeTable.objects.update_or_create(
        pk=pk,
        defaults={
            'change': change,
            'search': search,
        }
    )
    if created:
        result = {
            'error': False,
            'error_message': None,
            'access': 'Запись: "Заменить: "{}" Найти: "{}"" успешно добавлена'.format(obj.change, obj.search)
        }
    else:
        result = {
            'error': False,
            'error_message': None,
            'access': "Запись успешно обновлена"
        }
    return result
