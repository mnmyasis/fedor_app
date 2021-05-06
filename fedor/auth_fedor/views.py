import logging
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, HttpResponseRedirect

logger = logging.getLogger(__name__)

PATH_AUTH_JOINT_PAGE = 'auth_fedor/auth_joint_page.html'
REDIRECT_URL_AUTH_JOINT = 'auth_fedor:login_page'


def fedor_auth_for_ajax(func):
    """Декоратор проверки авторизации"""
    def wrapper(request):
        if request.user.is_authenticated:
            return func(request)
        else:
            raise PermissionDenied()

    return wrapper


def fedor_permit(perm=[1]):
    """Декоратор проверки авторизации и прав пользователя"""
    def wrapper(func):
        def permit(*args, **kwargs):
            request = args[0]
            if request.user.is_authenticated and request.user.profile.access_level.level in perm:
                return func(*args, **kwargs)
            else:
                if request.is_ajax():
                    raise PermissionDenied()
                else:
                    return redirect(REDIRECT_URL_AUTH_JOINT)

        return permit

    return wrapper


def show_login_page(request):
    """Показать страницу авторизации"""
    result = {'error': request.session.get('error')}
    return render(request, PATH_AUTH_JOINT_PAGE, result)


@require_http_methods(['POST'])
def user_login(request):
    """Авторизация пользователя"""
    res = {'username': request.POST.get('username'), 'password': request.POST.get('password')}
    user = auth.authenticate(username=res['username'], password=res['password'])
    if user:
        auth.login(request, user)
        logger.info('Авторизовался:{}'.format(request.user))
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
    next_page = request.GET['next']
    return HttpResponseRedirect(next_page)

