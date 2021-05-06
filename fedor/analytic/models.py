from django.db import models
from django.contrib.auth.models import User
from directory.models import Competitors


# Create your models here.

class MatchingStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.IntegerField()
    sku_id = models.IntegerField()
    eas_id = models.IntegerField()
    number_competitor = models.ForeignKey(Competitors, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'matching_statistic'

    # ACTION
    # 1 Ручной мэтчинг
    # 2 Ремэтчинг
    # 3 Изменение статуса мэтчинга
