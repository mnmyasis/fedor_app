from django.urls import path
from .views import *

app_name = 'admin_panel'
urlpatterns = [
    path('page/', show_admin_page, name="show_admin_page"),
    path('user/create/page/', show_registration_page, name='show_registration_page'),
    path('user/create/', user_registrations, name='create_user'),
    path('user/update/page/<int:user_id>', show_edit_user_page, name='show_edit_user_page'),
    path('user/update/<int:user_id>', update_user_profile, name='update_user_profile'),
    path('user/delete/<int:user_id>', delete_user, name='delete_user'),
    path('schedule/add-page/', schedule_add_page, name='schedule_add_page'),
    path('schedule/add/', schedule_add, name='schedule_add'),
    path('schedule/list/', schedule_list, name='schedule_list'),
    path('schedule/remove/<int:schedule_id>', schedule_remove, name='schedule_remove'),
    path('schedule/update-page/<int:schedule_id>', schedule_update_page, name='schedule_update_page'),
    path('schedule/update/<int:schedule_id>', schedule_update, name='schedule_update'),
    path('task/schedule-list/', task_schedule_list_page, name='task_schedule_list_page'),
    path('task/add-page/', task_add_page, name='task_add_page'),
    path('task/add/algoritm/', task_add_algoritm, name='task_add_algoritm'),
    path('task/remove/<int:task_id>', task_remove, name='task_remove'),
    path('task/change-status/<int:task_id>', task_change_status, name='task_change_status'),
    path('task-user/list/', tasks_user_list, name='tasks_user_list')

]