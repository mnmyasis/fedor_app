import logging
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, HttpResponseRedirect


## @defgroup auth_joint Авторизация пользователей
# @brief Модуль содержащий функции для работы с авторизацией пользователей
#  @param  PATH_AUTH_JOINT_PAGE - Глобальная переменная шаблона
#  @param  REDIRECT_URL_AUTH_JOINT - Глобальная переменная урла

## @ingroup auth_joint
#@{
logger = logging.getLogger(__name__)


PATH_AUTH_JOINT_PAGE = 'auth_joint/auth_joint_page.html'
REDIRECT_URL_AUTH_JOINT = 'auth_joint:login_page'

def show_login_page(request):
    """Показать страницу авторизации"""
    result = {'error': request.session.get('error')}
    return render(request, PATH_AUTH_JOINT_PAGE, result)

@require_http_methods(['POST'])
def user_login(request):
    """Авторизация пользователя"""
    res = {}
    res['username'] = request.POST.get('username')
    res['password'] = request.POST.get('password')
    user = auth.authenticate(username=res['username'], password=res['password'])
    if (user):
        auth.login(request, user)
        logger.info('Авторизовался:{}'.format(request.user))
        return redirect('/')
    else:
        logger.info('Ошибка авторизации {}'.format(res['username']))
        request.session['error'] = 'Неверно введены имя пользователя или пароль'
    return HttpResponseRedirect(
            reverse(REDIRECT_URL_AUTH_JOINT)
        )

def user_logout(request):
    """Деавторизация пользователя"""
    auth.logout(request)
    return redirect(REDIRECT_URL_AUTH_JOINT)

##@}