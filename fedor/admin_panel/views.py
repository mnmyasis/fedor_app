from datetime import datetime

import django_celery_results
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
import logging
from .models import Tasks
from .services import user_manipulation
from django.contrib.auth.models import User
from auth_fedor.views import fedor_permit, fedor_auth_for_ajax
from directory.models import Competitors
import json
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .services.forms.schedule_forms import CrontabScheduleForm
from directory.services.directory_querys import get_number_competitor_list
from django_celery_results.models import TaskResult

logger = logging.getLogger(__name__)

"""Глобальные переменные шаблонов"""
REGISTRATION_PAGE_TEMPLATE_PATH = 'admin_panel/registration_page.html'
UPDATE_USER_PROFILE_TEMPLATE_PATH = 'admin_panel/edit_user.html'
ADMIN_PAGE_PATH = 'admin_panel/admin_page.html'
SCHEDULE_TEMPLATE = 'admin_panel/add_schedule.html'
SCHEDULE_LIST_TEMPLATE = 'admin_panel/schedule_list.html'
SCHEDULE_UPDATE_TEMPLATE = 'admin_panel/schedule_update.html'
TASK_LIST_SCHEDULE_TEMPLATE = 'admin_panel/task_list_schedule.html'
TASK_ADD_SCHEDULE_TEMPLATE = 'admin_panel/task_add.html'

"""Глобальные переменные урлов"""
SHOW_REGISTRATION_PAGE_URL = 'admin_panel:show_registration_page'
SHOW_UPDATE_USER_PROFILE_PAGE_URL = 'admin_panel:show_edit_user_page'
SCHEDULE_ADD_URL = 'admin_panel:schedule_page'
SCHEDULE_LIST_URL = 'admin_panel:schedule_list'
TASK_LIST_SCHEDULE_URL = 'admin_panel:task_schedule_list_page'


def show_registration_page(request):
    """Рендер интерфейса регистрации пользовтеля"""
    result = {'error': request.session.get('error')}
    return render(request, REGISTRATION_PAGE_TEMPLATE_PATH, result)


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


@fedor_permit([1])
def show_edit_user_page(request, user_id):
    """Показывает интерфейс редактирования профиля"""
    logger.info('user_id: {}'.format(user_id))
    result = {
        'target_user': user_manipulation.get_user(user_id),
        'access_levels': user_manipulation.get_all_access_level(),
        'competitors': Competitors.objects.all(),
        'users': User.objects.all()
    }
    return render(request, UPDATE_USER_PROFILE_TEMPLATE_PATH, result)


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


@fedor_permit([1])
def delete_user(request, user_id):
    """Удаление четной записи пользователя"""
    User.objects.get(pk=user_id).delete()
    return HttpResponseRedirect(
        reverse(SHOW_UPDATE_USER_PROFILE_PAGE_URL,
                kwargs={'user_id': User.objects.latest('pk').pk})
    )


@fedor_permit([1])
def show_admin_page(request):
    """Рендер страници администрирования"""
    return render(request, ADMIN_PAGE_PATH, {})


@fedor_permit([1])
def schedule_add_page(request):
    """Рендер страницы добавления расписания"""
    result = {}
    return render(request, SCHEDULE_TEMPLATE, result)


@fedor_permit([1])
def schedule_add(request):
    """Добавить расписание"""
    request = json.loads(request.body.decode('utf-8'))
    date_start = request['data']['date']
    time_start = request['data']['time']
    if time_start:
        time_start = datetime.strptime(time_start, '%H:%M')
        hour = time_start.hour
        minute = time_start.minute
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
            timezone='Europe/Moscow'
        )
    return JsonResponse(True, safe=False)


@fedor_permit([1])
def schedule_remove(request, schedule_id):
    """Удалить расписание"""
    CrontabSchedule.objects.get(pk=schedule_id).delete()
    return HttpResponseRedirect(
        reverse(SCHEDULE_LIST_URL)
    )


def string_converter(value):
    """Конвертирование даты в строку для json.dumps"""
    return str(value)


@fedor_permit([1])
def schedule_list(request):
    """Список расписаний"""
    if request.is_ajax():
        schedules = CrontabSchedule.objects.all().values('minute', 'hour', 'day_of_week', 'month_of_year', 'timezone',
                                                         'pk')
        schedules = json.dumps(list(schedules), default=string_converter)
        return JsonResponse(schedules, safe=False)
    require = {
        'schedules': CrontabSchedule.objects.all().order_by('-pk')
    }
    return render(request, SCHEDULE_LIST_TEMPLATE, require)


@fedor_permit([1])
def schedule_update_page(request, schedule_id):
    """Страница редактирования расписания"""
    require = {
        'schedule': CrontabSchedule.objects.get(pk=schedule_id)
    }
    return render(request, SCHEDULE_UPDATE_TEMPLATE, require)


@fedor_permit([1])
@require_http_methods(['POST'])
def schedule_update(request, schedule_id):
    """Изменение расписания"""
    crontab_form = CrontabScheduleForm(request.POST, instance=CrontabSchedule.objects.get(pk=schedule_id))
    if crontab_form.is_valid():
        crontab_form.save()
        return HttpResponseRedirect(
            reverse(SCHEDULE_LIST_URL)
        )
    else:
        return HttpResponseRedirect(
            reverse(SCHEDULE_LIST_URL)
        )


@fedor_permit([1])
def task_schedule_list_page(request):
    """Страница задач"""
    require = {
        'tasks': PeriodicTask.objects.all().order_by('-total_run_count', '-pk'),
    }
    return render(request, TASK_LIST_SCHEDULE_TEMPLATE, require)


@fedor_permit([1])
def task_add_page(request):
    """Страница добавления задачи"""
    require = {
        'competitors': get_number_competitor_list(request.user),
    }
    return render(request, TASK_ADD_SCHEDULE_TEMPLATE, require)


@fedor_permit([1])
def task_add_algoritm(request):
    """Добавление в планировщик задач алгоритма"""
    request = json.loads(request.body.decode('utf-8'))
    number_competitor_id = json.loads(request['data'].get('number_competitor_id'))
    name = request['data'].get('name')
    description = request['data'].get('description')
    crontab = request['data'].get('crontab')
    new_sku = request['data'].get('new_sku')
    action = request['data'].get('action')
    barcode_match = request['data'].get('barcode_match')
    task_status = request['data'].get('task_status')
    one_task_status = request['data'].get('one_task_status')
    selected_task = request['data'].get('selected_task')

    arguments = {
        'number_competitor_id': number_competitor_id,
        'new_sku': new_sku,
        'action': action,
        'barcode_match': barcode_match
    }
    PeriodicTask.objects.create(
        crontab=CrontabSchedule.objects.get(pk=crontab),
        name=name,
        description=description,
        task=selected_task,
        kwargs=json.dumps(arguments),
        enabled=task_status,
        one_off=one_task_status
    )
    return JsonResponse(True, safe=False)


@fedor_permit([1])
def task_remove(request, task_id):
    """Удаление задачи"""
    PeriodicTask.objects.get(pk=task_id).delete()
    return HttpResponseRedirect(
        reverse(TASK_LIST_SCHEDULE_URL)
    )


@fedor_permit([1])
def task_change_status(request, task_id):
    """Изменение статуса задачи"""
    task = PeriodicTask.objects.get(pk=task_id)
    if task.enabled:
        task.enabled = False
    else:
        task.enabled = True
    task.save()
    return HttpResponseRedirect(
        reverse(TASK_LIST_SCHEDULE_URL)
    )


def tasks_user_list(request):
    """Список задач в интерфейсе АВТОМЭТЧИНГ"""
    tasks = Tasks.objects.filter(user=request.user).order_by('-pk', 'status', ).values('name', 'create_date',
                                                                                       'user__username', 'status',
                                                                                       'result',
                                                                                       'task_id')
    result = []
    for task in tasks:
        try:
            task_result = TaskResult.objects.get(task_id=task['task_id'])
        except django_celery_results.models.TaskResult.DoesNotExist:
            Tasks.objects.get(task_id=task['task_id']).delete()
            continue
        tsk = Tasks.objects.get(task_id=task_result.task_id)
        tsk.status = task_result.status
        tsk.result = '{}'.format(task_result.result)
        tsk.save()
        result.append({
            'name': tsk.name,
            'create_date': tsk.create_date.strftime('%d-%m-%Y %H:%M'),
            'user__username': tsk.user.username,
            'status': tsk.status,
            'result': tsk.result,
        })
    tasks = json.dumps(result, default=string_converter)
    return JsonResponse(tasks, safe=False)
