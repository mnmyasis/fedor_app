from .forms.create_update_user_forms import CustomCreationForm, CustomUpdateUserForm
from django.contrib.auth.models import User
from admin_panel.models import *
import logging

logger = logging.getLogger(__name__)

## @defgroup service_registartion_user Сервис создания пользователя
## @ingroup registartion_user
# @{

## @details создает пользователя в БД
#  @param[in] request.POST
#  @param[out] user_id
#  @param[out] False
def create_user(request_post):
    """Создание пользовтеля"""
    user_creation_form = CustomCreationForm(request_post)
    if user_creation_form.is_valid():
        logger.debug('Форма регистрации прошла валидность')
        user = user_creation_form.save()
        return user.id
    else:
        logger.debug('Форма регистрации не прошла проверку на валидность')
        return False

##@}

## @defgroup service_update_user_profile Сервис редактирования пользовательского профиля
## @ingroup update_user_profile
# @{

## @details Редактирование профиля пользователя
#  @param[in] request_post - POST запрос
#  @param[in] user_id - Пользовательский id
#  @param[in] access_level - Уровень доступа
def edit_user_profile(request_post, user_id=None, access_level=1):
    """Редактирование профиля пользователя"""
    logger.debug('user_id: {}, access_level_id: {}'.format(user_id, access_level))
    update_form = CustomUpdateUserForm(request_post, instance=get_user(user_id))
    if update_form.is_valid():
        logger.debug('Валидность формы пройдена')
        update_form.save(access_level)
        return True
    else:
        logger.debug('Форма не прошла проверку на валидность')
        return False

##@}

## @defgroup get_user Выгрузка пользователя
#  @ingroup show_update_user_profile
#  @ingroup service_update_user_profile

## @ingroup get_user
# @{
## @details Выгрузка пользователя из БД django.contrib.auth.models.User
#  @param[in] user_id принимает id
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        logger.error('Пользователь с id {} не найден'.format(user_id))
        return False

##@}

## @defgroup get_access_level_all Выгрузка всех уровней доступа
#  @ingroup show_update_user_profile

## @ingroup get_access_level_all
# @{
## @details Выгрузка прав из БД
def get_all_access_level():
    access_levels = AccessLevel.objects.all()
    return access_levels

##@}
