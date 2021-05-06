from .forms.create_update_user_forms import CustomCreationForm, CustomUpdateUserForm
from django.contrib.auth.models import User
from admin_panel.models import *
import logging

logger = logging.getLogger(__name__)


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


def edit_user_profile(request_post, user_id=None, access_level=1, competitor=None):
    """Редактирование профиля пользователя"""
    logger.debug('user_id: {}, access_level_id: {}'.format(user_id, access_level))
    update_form = CustomUpdateUserForm(request_post, instance=get_user(user_id))
    if update_form.is_valid():
        logger.debug('Валидность формы пройдена')
        update_form.save(access_level, competitor)
        return True
    else:
        logger.debug('Форма не прошла проверку на валидность')
        return False


def get_user(user_id):
    """Получить пользователя"""
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        logger.error('Пользователь с id {} не найден'.format(user_id))
        return False


def get_all_access_level():
    """Уровни доступов"""
    access_levels = AccessLevel.objects.all()
    return access_levels
