from analytic.models import MatchingStatistic
from django.contrib.auth.models import User
from directory.models import NumberCompetitor, ClientDirectory
from manual_matching.models import ManualMatchingData, FinalMatching


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
    return statistic


def status_matchings(date, number_competitor=1):
    statistic = {
        'progress': ManualMatchingData.objects.filter(number_competitor=number_competitor, create_date=date).count()
    }
    for status in range(1, 7):
        count = FinalMatching.objects.filter(number_competitor=number_competitor, create_date=date,
                                             type_binding=status).count()
        statistic.update(__stat(status, count))
    return statistic


def status_changes(date, number_competitor):
    statistic = {}
    for status in range(1, 7):
        count = FinalMatching.objects.filter(number_competitor=number_competitor, update_date=date,
                                             type_binding=status).count()
        statistic.update(__stat(status, count))
    return statistic


def status_user_changes(date, number_competitor):
    statistic = []
    users = User.objects.all()
    for user in users:
        for status in range(1, 7):
            count = FinalMatching.objects.filter(number_competitor=number_competitor, update_date=date,
                                                 type_binding=status, user=user).count()
            statistic.append(
                {
                    'user': user.last_name,
                    'statistic': __stat(status, count)
                }
            )
    return statistic


def user_rating(number_competitor):
    statistic = []
    users = User.objects.all()
    for user in users:
        count = MatchingStatistic.objects.filter(number_competitor=number_competitor, user=user).count()
        statistic.append({
            'user': user,
            'count': count
        })
    return statistic


def not_used_sku(number_competitor):
    count = ClientDirectory.objects.filter(number_competitor=number_competitor, matching_status=False).cpunt()
    return count
