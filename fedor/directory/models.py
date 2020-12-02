from django.db import models


class GroupChangeTable(models.Model):
    change = models.TextField(blank=True)
    search = models.TextField()

    class Meta:
        db_table = 'group_change_table'


class NumberCompetitor(models.Model):
    """СКУ справочники"""
    name = models.TextField(default='test')

    class Meta:
        db_table = 'number_competitor'


class ClientDirectory(models.Model):
    """СКУ справочник"""
    nnt = models.IntegerField()
    name = models.TextField()
    matching_status = models.BooleanField(default=False)
    number_competitor = models.ForeignKey(NumberCompetitor, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_directory'
        ordering = ['nnt']


class BaseDirectory(models.Model):
    """ЕАС справочник"""

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
