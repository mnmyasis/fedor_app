from django.db import models


class GroupChangeTable(models.Model):
    change = models.TextField(blank=True)  # На что нужно заменить
    search = models.TextField()  # Что нужно заменить

    class Meta:
        db_table = 'group_change_table'


class NumberCompetitor(models.Model):
    """СКУ справочники тестовый"""
    name = models.TextField(default='test')

    class Meta:
        db_table = 'number_competitor'


class ClientDirectory(models.Model):
    """СКУ справочник тестовый"""
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
    """ЕАС справочник тестовый"""

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


class SyncEAS(models.Model):
    eas_id = models.BigIntegerField()
    status = models.IntegerField(default=1)
    barcode = models.TextField(blank=True, null=True)
    umbrella_brand = models.TextField(blank=True, null=True)
    tn_fv = models.TextField(blank=True, null=True)
    registration_tm = models.TextField(blank=True, null=True)
    corporation = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)
    rx_otc = models.TextField(blank=True, null=True)
    trade_name_rus = models.TextField(blank=True, null=True)
    trade_name_eng = models.TextField(blank=True, null=True)
    pack_key = models.TextField(blank=True, null=True)
    fv_short = models.TextField(blank=True, null=True)
    type_packing_fv = models.TextField(blank=True, null=True)
    dosage = models.TextField(blank=True, null=True)
    volwe = models.TextField(blank=True, null=True)
    numero = models.TextField(blank=True, null=True)
    tastes_and_parentheses_fv = models.TextField(blank=True, null=True)
    vendor_code = models.TextField(blank=True, null=True)
    divisible_packaging = models.TextField(blank=True, null=True)
    size = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    full_corp = models.TextField(blank=True, null=True)
    corp_rus = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'sync_eas'


class EAS(models.Model):
    """Не используется"""
    eas_id = models.BigIntegerField()
    status = models.IntegerField(default=1)
    barcode = models.TextField(blank=True, null=True)
    umbrella_brand = models.TextField(blank=True)
    tn_fv = models.TextField(blank=True)
    registration_tm = models.TextField(blank=True)
    corporation = models.TextField(blank=True)
    manufacturer = models.TextField(blank=True)
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
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'eas'


class Competitors(models.Model):
    """СКУ СПРАВОЧНИКИ"""
    name = models.TextField(default='test')
    pharmacy_id = models.BigIntegerField()
    firm_id = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'competitors'


class SKU(models.Model):
    """СКУ НОМЕНКЛАТУРА"""
    """Не используется"""
    sku_id = models.BigIntegerField()
    nnt = models.TextField(blank=True)
    name = models.TextField()
    matching_status = models.BooleanField(default=False)
    number_competitor = models.ForeignKey(Competitors, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sku'
        ordering = ['sku_id']


class SyncSKU(models.Model):
    """СКУ НОМЕНКЛАТУРА"""
    sku_id = models.BigIntegerField()
    nnt = models.TextField(blank=True)
    name = models.TextField()
    matching_status = models.BooleanField(default=False)
    number_competitor = models.ForeignKey(Competitors, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sync_sku'
        ordering = ['sku_id']