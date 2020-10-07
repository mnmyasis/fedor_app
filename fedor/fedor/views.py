from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)


# @login_required(login_url='/auth/login/')
def index(request):
    return render(request, 'index.html')


def change_style_interface(request):
    """Смена стиля интерфейса"""
    is_dark = request.session.get('is_dark_style')
    if is_dark:
        logger.debug('Светлая тема: is_dark_style = {}'.format(is_dark))
        is_dark = False
    else:
        logger.debug('Темная тема: is_dark_style = {}'.format(is_dark))
        is_dark = True
    request.session['is_dark_style'] = is_dark
    return redirect('/')
