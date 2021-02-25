from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from admin_panel.models import *


## @defgroup form_registartion_user Форма создания пользователя
#  @details Форма создания пользователя в БД CustomCreationForm
#  @ingroup service_registartion_user
# @{

class CustomCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1']

    ##  @details Создается юзер и связь между User и AccessLevel в Profile
    def save(self):
        user = super(CustomCreationForm, self).save(commit=True)
        Profile.objects.create(
            user=user,
            access_level=AccessLevel.objects.get(id=1))  # Права по умолчанию
        return user


##@}


## @defgroup form_update_user_profile Форма редактирования пользовательского профиля
#  @details Форма редактирования пользовательского профиля CustomUpdateUserForm
#  @ingroup service_update_user_profile
# @{

class CustomUpdateUserForm(UserChangeForm):
    """Форма редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    ##  @param[in] level_id - уровень доступа
    def save(self, level_id):
        user = super(CustomUpdateUserForm, self).save(commit=True)
        access_level = AccessLevel.objects.get(level=level_id)
        try:
            profile = Profile.objects.get(user=user)
            profile.access_level = access_level
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, access_level=access_level)
        return user
##@}
