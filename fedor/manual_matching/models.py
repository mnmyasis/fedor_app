from django.contrib.auth.models import User
from django.db import models


class ManualMatchingData(models.Model):
    id_sku_dict = models.BigIntegerField(blank=True)
    id_eas_dict = models.BigIntegerField(blank=True)
    name_eas = models.TextField(blank=True)
    name_sku = models.TextField(blank=True)
    lvl = models.FloatField(blank=True)
    lvl2 = models.FloatField(blank=True)
    perc_num = models.FloatField(blank=True)
    matching_status = models.BooleanField(default=False)
    number_competitor = models.IntegerField(default=1)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    date_update = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manual_matching_data'
