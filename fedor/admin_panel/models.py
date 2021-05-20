from django.db import models
from django.contrib.auth.models import User
from directory.models import Competitors


class AccessLevel(models.Model):
    """Уровень доступа"""
    level = models.IntegerField()
    level_name = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.level_name)

    # level 1 level_name Админ
    # level 2 level_name Суперюзер
    # level 3 level_name Сотрудник pharma.Global
    # level 4 level_name Аптека


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitors, models.SET_NULL, blank=True, null=True)


class Tasks(models.Model):
    """Пользовательские задачи"""
    task_id = models.CharField(max_length=500)
    name = models.TextField()
    status = models.CharField(max_length=500, blank=True)
    result = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=1)


class FedorLog(models.Model):
    message = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sku_id = models.BigIntegerField(blank=True, null=True)
    eas_id = models.BigIntegerField(blank=True, null=True)
    action = models.IntegerField()  # 1 мэтчинг, 2 запуск алгоритма, 3 массовые подмены, 4 планировщик
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fedor_log'
        ordering = ['-create_date']
