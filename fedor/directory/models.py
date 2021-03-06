from django.db import models


class GroupChangeTable(models.Model):
    change = models.TextField(blank=True)  # На что нужно заменить
    search = models.TextField()  # Что нужно заменить

    class Meta:
        db_table = 'group_change_table'


class SyncEAS(models.Model):
    eas_id = models.BigIntegerField()
    status = models.IntegerField(default=1)  # Список статусов ниже в комментариях
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

    # 1 Валидировано
    # 2 Помечен на удаление
    # 3 Модерация.Позиция заведена через акцию
    # 4 Модерация.Загрузка из шаблона
    # 5 Валидировано с замечаниями
    # 6 На модерацию
    # 7 на модерацию.Предложено добавить из Федора

    class Meta:
        db_table = 'sync_eas'

    def __str__(self):
        return str(self.eas_id)


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return str(self.sku_id)
