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


class FinalMatching(models.Model):
    id_sku_dict = models.BigIntegerField()
    id_eas_dict = models.BigIntegerField()
    type_binding = models.IntegerField()
    name_binding = models.TextField(blank=True)
    old_type_binding = models.IntegerField(blank=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    number_competitor = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    '''
    type_binding:
        1 - алгоритм
        2 - алгоритм + ручная
        3 - ручная
        4 - алгоритм не нашел бренд
        5 - предложить добавить
        6 - согласовано на добавление
        8 - не один вариант алгоритма не подошел
        21 - алгоритм закинул в топ, не верный элемент 
        666 - мусор
    '''

    class Meta:
        db_table = 'final_matching'
        ordering = ['id_sku_dict']