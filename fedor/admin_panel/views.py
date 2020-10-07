from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import logging
from .services import user_manipulation

## @defgroup admin_joint Администрирование стыковщика
# @brief Основной модуль, содержащий в себе модули для работы с пользователями


logger = logging.getLogger(__name__)

## @defgroup registration - Регистрация пользователя
#  @brief Основной модуль, содержащий в себе модули регистрации пользователя
#  @ingroup admin_joint

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
#  @ingroup admin_joint

## @defgroup show_update_user_profile Рендеринг страницы редактирования пользовательского профиля
#  @ingroup edit_user
#  @param UPDATE_USER_PROFILE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_UPDATE_USER_PROFILE_PAGE_URL - Глобальная переменная урла

## @defgroup update_user_profile Редактирование пользовательского профиля
#  @ingroup edit_user
#  @param UPDATE_USER_PROFILE_TEMPLATE_PATH - Глобальные переменная шаблона
#  @param SHOW_UPDATE_USER_PROFILE_PAGE_URL - Глобальная переменная урла


"""Глобальные переменные шаблонов"""
REGISTRATION_PAGE_TEMPLATE_PATH = 'admin_joint/registration_page.html'
UPDATE_USER_PROFILE_TEMPLATE_PATH = 'admin_joint/update_user_profile_page.html'

"""Глобальные переменные урлов"""
SHOW_REGISTRATION_PAGE_URL = 'admin_joint:show_registration_page'
SHOW_UPDATE_USER_PROFILE_PAGE_URL = 'admin_joint:show_update_user_profile_page'




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
## @details Принимает POST запрос регистрации пользователя
@require_http_methods(['POST'])
def user_registrations(request):
    """Регистрация пользователя"""
    user_id = user_manipulation.create_user(request.POST)
    if user_id:
        logger.debug('Пользователь успешно создан')
        return HttpResponseRedirect(
            reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                    kwargs={'user_id': user_id})
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
def show_update_user_profile_page(request, user_id):
    """Показывает интерфейс редактирования профиля"""
    logger.info('user_id: {}'.format(user_id))
    result = {
        'target_user': user_manipulation.get_user(user_id),
        'access_levels': user_manipulation.get_all_access_level()
    }
    return render(request, UPDATE_USER_PROFILE_TEMPLATE_PATH, result)

##@}

## @ingroup update_user_profile
# @{
#  @details Контроллер редактирование пользователя
#  @param[in] user_id - принимает user_id
#  @param[in] POST.get('access_level') - выбранный уровень доступа
#  @param request.POST - содержит поля стандартной модели User
@require_http_methods(['POST'])
def update_user_profile(request, user_id):
    """Изменение профиля пользовтеля"""
    access_level = request.POST.get('access_level')
    if user_manipulation.edit_user_profile(request.POST, user_id, access_level):
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
