from django.contrib.auth.models import User
from django.db import models


# Create your models here.

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
