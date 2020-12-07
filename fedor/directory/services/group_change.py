import json
import re
from datetime import datetime
from directory.models import ClientDirectory, GroupChangeTable
from django.db.models import Q


def __replace_line(line, change_lines):
    old_name = line.name
    new_name = ''
    for ch_line in change_lines:
        line.name = re.sub(r'\s(,)\s', ' ', line.name)  # Удаление запятых
        line.name = re.sub(r'(,)\s', ' ', line.name)  # Удаление запятых
        counter_equality = 0  # Счетчик кол-ва совпавших букв нскз с подменой
        string = 0  # Первое совпадение букв ску с подменами
        for x in range(0, len(line.name)):  # Побуквенное сравнивание
            """Здесь должны совпасть подряд все символы подмены с подстрокой ску"""
            if line.name[x] == ch_line.search[counter_equality]:  # Если буква совпала
                if counter_equality == 0: string = x  # Запись id первого совпадения
                if counter_equality <= len(ch_line.search): counter_equality += 1  # Переход на след букву строки подмен
                if counter_equality == len(ch_line.search):  # Счетчик совпавших букв подмены равен длинне строки
                    if len(line.name) == x + 1:  # Конец строки ску
                        if ' ' == line.name[string-1]:  # Есть ли пробел перед подстрокой ску
                            change = True
                        else:
                            change = False
                    else:
                        if ' ' == line.name[string-1] and ' ' == line.name[x + 1]: # Есть ли пробел перед/после подстрокой ску
                            change = True
                        else:
                            change = False
                    if change:  # Есть ли пробел перед подстрокой ску

                        """:string от начала строки до первого совпадения, подмена, x+1:len(line.name) всё после подмены"""
                        new_name = line.name[:string] + ch_line.change + line.name[x + 1: len(line.name)]
                        break
                    else:  # Сброс счетчиков, подстрока является частью другого слова
                        string = ''
                        counter_equality = 0
            else:  # Если буква не совпала сброс счетчиков
                string = ''
                counter_equality = 0
    # line.save()
    print('old: {}---->new: {}'.format(old_name, new_name))
    return True


def change_line(number_competitor, exclude_list):
    start = datetime.now()
    names = ClientDirectory.objects.filter(number_competitor=number_competitor).extra(select={'length': 'Length(name)'}).order_by('-length')
    change_lines = GroupChangeTable.objects.exclude(pk__in=[exclude.pk for exclude in exclude_list])
    for name in names:
        __replace_line(name, change_lines)
    end = datetime.now()
    result_time = end - start
    print('Потрачено времени - {}'.format(result_time))


def get_group_changes(group_changes_input):
    changes_list = GroupChangeTable.objects.filter(search__icontains=group_changes_input)[:10].values('pk', 'search')
    changes_list = json.dumps(list(changes_list))
    return changes_list
