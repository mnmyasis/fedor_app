import logging
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, HttpResponseRedirect

## @defgroup auth_fedor Авторизация пользователей
# @brief Модуль содержащий функции для работы с авторизацией пользователей
#  @param  PATH_AUTH_JOINT_PAGE - Глобальная переменная шаблона
#  @param  REDIRECT_URL_AUTH_JOINT - Глобальная переменная урла

## @ingroup auth_fedor
# @{
logger = logging.getLogger(__name__)

PATH_AUTH_JOINT_PAGE = 'auth_fedor/auth_joint_page.html'
REDIRECT_URL_AUTH_JOINT = 'auth_fedor:login_page'


def show_login_page(request):
    """Показать страницу авторизации"""
    next = request.GET.get('next')  # Для передачи урла предыдущей страницы в POST запросе.
    result = {'error': request.session.get('error'), 'next': next}
    return render(request, PATH_AUTH_JOINT_PAGE, result)


@require_http_methods(['POST'])
def user_login(request):
    """Авторизация пользователя"""
    res = {'username': request.POST.get('username'), 'password': request.POST.get('password')}
    user = auth.authenticate(username=res['username'], password=res['password'])
    if user:
        auth.login(request, user)
        logger.info('Авторизовался:{}'.format(request.user))

        previous_url = request.GET.get('next')
        if previous_url and previous_url != 'None':  # Если есть путь на страницу, с которой пользователя средиректило
            return redirect(previous_url)  # Возварт к предыдущей странице
        return redirect('/matching/manual-matching/page/')
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
