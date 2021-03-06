from django.contrib.auth.models import User
from django.db import models
from directory.models import SyncSKU, SyncEAS, Competitors


class ManualMatchingData(models.Model):
    sku_dict = models.ForeignKey(SyncSKU, on_delete=models.CASCADE)
    eas_dict = models.ForeignKey(SyncEAS, on_delete=models.CASCADE)
    name_eas = models.TextField(blank=True)
    name_sku = models.TextField(blank=True)
    lvl = models.FloatField(blank=True)
    lvl2 = models.FloatField(blank=True)
    perc_num = models.FloatField(blank=True)
    matching_status = models.BooleanField(default=False)
    number_competitor = models.IntegerField(default=1)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'manual_matching_data'


class FinalMatching(models.Model):
    sku_dict = models.ForeignKey(SyncSKU, on_delete=models.CASCADE)
    eas_dict = models.ForeignKey(SyncEAS, models.SET_NULL, blank=True, null=True)
    type_binding = models.IntegerField()
    name_binding = models.TextField(blank=True)
    old_type_binding = models.IntegerField(blank=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    number_competitor = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'final_matching'

# 1 Мэтчинг по ШК - требуется проверка
# 2 Мэтчинг по ШК - проверка не требуется
# 3 Мэтчинг вручную
# 4 Не найдено соответствие в ЕАС
# 5 Предложено к добавлению в ЕАС
# 6 Прочее
# 7 Смэтчено аптекой
# 8 Алгоритм
