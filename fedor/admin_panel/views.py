from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import logging
from .services import user_manipulation
from django.contrib.auth.models import User
from auth_fedor.views import fedor_permit
from directory.models import NumberCompetitor

## @defgroup admin_panel Администрирование стыковщика
# @brief Основной модуль, содержащий в себе модули для работы с пользователями


logger = logging.getLogger(__name__)

## @defgroup registration - Регистрация пользователя
#  @brief Основной модуль, содержащий в себе модули регистрации пользователя
#  @ingroup admin_panel

## @defgroup show_registartion_user Рендеринг страницы регистрации
#  @ingroup registration
#  @param REGISTRATION_PAGE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_REGISTRATION_PAGE_URL - Глобальная переменная урла

## @defgroup registartion_user Создание пользователя
#  @ingroup registration
#  @param REGISTRATION_PAGE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_REGISTRATION_PAGE_URL - Глобальная переменная урла

## @defgroup edit_user - Редактирование пользователя
#  @brief Основной модуль, содержащий в себе модули работы с редактирование профиля
#  @ingroup admin_panel

## @defgroup show_update_user_profile Рендеринг страницы редактирования пользовательского профиля
#  @ingroup edit_user
#  @param UPDATE_USER_PROFILE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_UPDATE_USER_PROFILE_PAGE_URL - Глобальная переменная урла

## @defgroup update_user_profile Редактирование пользовательского профиля
#  @ingroup edit_user
#  @param UPDATE_USER_PROFILE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_UPDATE_USER_PROFILE_PAGE_URL - Глобальная переменная урла


"""Глобальные переменные шаблонов"""
REGISTRATION_PAGE_TEMPLATE_PATH = 'admin_panel/registration_page.html'
UPDATE_USER_PROFILE_TEMPLATE_PATH = 'admin_panel/edit_user.html'
ADMIN_PAGE_PATH = 'admin_panel/admin_page.html'

"""Глобальные переменные урлов"""
SHOW_REGISTRATION_PAGE_URL = 'admin_panel:show_registration_page'
SHOW_UPDATE_USER_PROFILE_PAGE_URL = 'admin_panel:show_edit_user_page'


## @ingroup show_registartion_user
# @{

## @details Рендер интерфейса регистрации пользовтеля
#  @param request.session в сессии с ключом "error" передаются ошибки
def show_registration_page(request):
    result = {'error': request.session.get('error')}
    return render(request, REGISTRATION_PAGE_TEMPLATE_PATH, result)


##@}

## @ingroup registartion_user
# @{
## @details
@require_http_methods(['POST'])
def user_registrations(request):
    """Регистрация пользователя"""
    user_id = user_manipulation.create_user(request.POST)
    if user_id:
        if request.user.is_authenticated:
            logger.debug('Пользователь успешно создан')
            return HttpResponseRedirect(
                reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                        kwargs={'user_id': user_id})
                )
        else:
            return HttpResponseRedirect(
                reverse('auth_fedor:login_page')
            )
    request.session['error'] = 'Вы ввели невалидный пароль!'
    logger.debug('Не удалось создать пользователя')
    return HttpResponseRedirect(
        reverse(SHOW_REGISTRATION_PAGE_URL)
    )


##@}


## @ingroup show_update_user_profile
# @{
#  @param[in] user_id передается в GET
@login_required
@fedor_permit([1])
def show_edit_user_page(request, user_id):
    """Показывает интерфейс редактирования профиля"""
    logger.info('user_id: {}'.format(user_id))
    result = {
        'target_user': user_manipulation.get_user(user_id),
        'access_levels': user_manipulation.get_all_access_level(),
        'competitors': NumberCompetitor.objects.all(),
        'users': User.objects.all()
    }
    return render(request, UPDATE_USER_PROFILE_TEMPLATE_PATH, result)


##@}

## @ingroup update_user_profile
# @{
#  @details Контроллер редактирование пользователя
#  @param[in] user_id - принимает user_id
#  @param[in] POST.get('access_level') - выбранный уровень доступа
#  @param request.POST - содержит поля стандартной модели User
@login_required
@fedor_permit([1])
def update_user_profile(request, user_id):
    """Изменение профиля пользовтеля"""
    request.session['error'] = ''
    access_level = request.POST.get('access_level')
    competitor = request.POST.get('competitor')
    if user_manipulation.edit_user_profile(request.POST, user_id, access_level, competitor):
        logger.debug('Профиль успешно обновлен!')
        return HttpResponseRedirect(
            reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                    kwargs={'user_id': user_id})
        )
    else:
        request.session['error'] = 'Не удалось внести изменения'
        logger.debug('Не удалось обновить профиль')
        return HttpResponseRedirect(
            reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                    kwargs={'user_id': user_id})
        )


##@}


@login_required
@fedor_permit([1])
def delete_user(request, user_id):
    User.objects.get(pk=user_id).delete()
    return HttpResponseRedirect(
        reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                kwargs={'user_id': User.objects.latest('pk').pk})
    )

@login_required
def show_admin_page(request):
    return render(request, ADMIN_PAGE_PATH, {})
