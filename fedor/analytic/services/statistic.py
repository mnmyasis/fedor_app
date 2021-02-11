from analytic.models import MatchingStatistic
from django.contrib.auth.models import User
from directory.models import NumberCompetitor, ClientDirectory
from manual_matching.models import ManualMatchingData, FinalMatching
from datetime import datetime, timedelta


def statistic_write(user_id, sku_id, eas_id, number_competitor, action):
    MatchingStatistic.objects.create(
        user=User.objects.get(pk=user_id),
        sku_id=sku_id,
        eas_id=eas_id,
        number_competitor=NumberCompetitor.objects.get(pk=number_competitor),
        action=action
    )
    return True


def __stat(status, count):
    statistic = {}
    if status == 1:
        statistic['barcode_check'] = count
    elif status == 2:
        statistic['barcode_not_check'] = count
    elif status == 3:
        statistic['manual'] = count
    elif status == 4:
        statistic['not_found'] = count
    elif status == 5:
        statistic['add_eas'] = count
    elif status == 6:
        statistic['other'] = count
    elif status == 7:
        statistic['drugstore'] = count
    elif status == 8:
        statistic['algoritm'] = count
    return statistic


def status_matchings(start_date, end_date, number_competitor=1):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    statistic = {
        'progress': ManualMatchingData.objects.filter(
            number_competitor=number_competitor, create_date__gte=start_date, create_date__lte=end_date).count()
    }
    for status in range(1, 7):
        count = FinalMatching.objects.filter(number_competitor=number_competitor,
                                             create_date__gte=start_date, create_date__lte=end_date,
                                             type_binding=status).count()
        statistic.update(__stat(status, count))
    return statistic


def status_changes(start_date, end_date, number_competitor):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date = start_date
    statistic = []
    while date < end_date:
        stats = {
            'date': datetime.strftime(date, '%Y-%m-%d'),
            'statistic': {}
        }
        _date = datetime.strftime(date, '%Y-%m-%d')
        for status in range(1, 9):
            count = FinalMatching.objects.filter(number_competitor=number_competitor,
                                                 update_date__contains=_date,
                                                 type_binding=status).count()
            stats['statistic'].update(__stat(status, count))
        statistic.append(stats)
        date = date + timedelta(1)
    return statistic


def status_user_changes(start_date, end_date, number_competitor):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    statistic = []
    users = User.objects.all()
    for user in users:
        stats = {
            'user': user.username,
            'statistic': {}
        }
        for status in range(1, 7):
            count = FinalMatching.objects.filter(number_competitor=number_competitor,
                                                 update_date__gte=start_date, update_date__lte=end_date,
                                                 type_binding=status, user=user).count()
            stats['statistic'].update(__stat(status, count))
        statistic.append(stats)
    return statistic


def user_rating(start_date, end_date, number_competitor):

    statistic = []
    users = User.objects.all()
    for user in users:
        count = MatchingStatistic.objects.filter(number_competitor=number_competitor,
                                                 create_date__range=(start_date, end_date),
                                                 user=user).count()
        statistic.append({
            'user': user.username,
            'count': count
        })
    return statistic


def load_raw_sku(start_date, end_date):
    statistic = []
    number_competitors = NumberCompetitor.objects.all()
    for number_competitor in number_competitors:
        raw_count = ClientDirectory.objects.filter(
            number_competitor=number_competitor,
            matching_status=False,
            create_date__range=(start_date, end_date)
        ).count()
        statistic.append({
            'number_competitor': number_competitor.name,
            'raw_count': raw_count
        })
    return statistic
