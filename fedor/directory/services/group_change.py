from datetime import datetime
from directory.models import ClientDirectory, GroupChangeTable


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




