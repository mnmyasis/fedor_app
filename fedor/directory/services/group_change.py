from datetime import datetime
from directory.models import ClientDirectory, GroupChangeTable
import json


def __replace_line(line, change_lines):
    print(line.name)
    for ch_line in change_lines:
        line.name = line.name.replace(ch_line.search, ch_line.change)
    print(line.name)
    print(line.pk)
    line.save()


def change_line(number_competitor):
    start = datetime.now()
    names = ClientDirectory.objects.filter(number_competitor=number_competitor).extra(select={'length': 'Length(name)'})\
        .order_by('-length')
    change_lines = GroupChangeTable.objects.all()
    for name in names:
        __replace_line(name, change_lines)
    end = datetime.now()
    result_time = end - start
    print('Потрачено времени - {}'.format(result_time))


def get_group_changes(group_changes_input):
    changes_list = GroupChangeTable.objects.filter(change__icontains=group_changes_input)[:10].values('pk', 'change')
    changes_list = json.dumps(list(changes_list))
    return changes_list

