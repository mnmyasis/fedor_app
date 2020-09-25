from django.db import models
from django.contrib.auth.models import User

## @defgroup access_level_model
#  @ingroup get_access_level_all
#  @ingroup form_update_user_profile
#  @ingroup form_registartion_user

## @ingroup access_level_model
# @{
# @details Таблица уровней доступа
class AccessLevel(models.Model):
    """Уровень доступа"""
    level = models.IntegerField()
    level_name = models.CharField(max_length=150)

    def __str__(self):
        return '{}'.format(self.level_name)

##@}

## @defgroup profile_model
#  @ingroup form_update_user_profile
#  @ingroup form_registartion_user

## @ingroup profile_model
# @{
#  @details Таблица для связки юзера и уровня доступа
class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
##@}
