from django.db import models


class ClientDirectory(models.Model):
    """Клиентский справочник"""
    nnt = models.IntegerField()
    name = models.TextField()
    joint_status = models.BooleanField(default=False)
    number_competitor = models.IntegerField()

    class Meta:
        db_table = 'client_directory'
        ordering = ['nnt']


class BaseDirectory(models.Model):
    """Базовый справочник"""

    umbrella_brand = models.TextField(blank=True)
    source = models.TextField(blank=True)
    tn_fv = models.TextField(blank=True)
    registration_tm = models.TextField(blank=True)
    corporation = models.TextField(blank=True)
    manufacturer = models.TextField(blank=True)
    country = models.TextField(blank=True)
    rx_otc = models.TextField(blank=True)
    trade_name_rus = models.TextField(blank=True)
    trade_name_eng = models.TextField(blank=True)
    pack_key = models.TextField(blank=True)
    fv_short = models.TextField(blank=True)
    type_packing_fv = models.TextField(blank=True)
    dosage = models.TextField(blank=True)
    volwe = models.TextField(blank=True)
    numero = models.TextField(blank=True)
    tastes_and_parentheses_fv = models.TextField(blank=True)
    vendor_code = models.TextField(blank=True)
    divisible_packaging = models.TextField(blank=True)
    size = models.TextField(blank=True)
    age = models.TextField(blank=True)
    full_corp = models.TextField(blank=True)
    corp_rus = models.TextField(blank=True)

    class Meta:
        db_table = 'base_directory'

    def get_filter_fields(self):
        """Получить имена полей базового справочника"""
        fields = [x.name for x in self._meta.get_fields()]
        return fields
