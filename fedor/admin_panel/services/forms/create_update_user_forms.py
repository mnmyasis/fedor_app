from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from directory.models import Competitors
from admin_panel.models import *


class CustomCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1']

    def save(self):
        user = super(CustomCreationForm, self).save(commit=True)
        Profile.objects.create(
            user=user,
            access_level=AccessLevel.objects.get(id=3))  # Права по умолчанию
        return user


class CustomUpdateUserForm(UserChangeForm):
    """Форма редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, level_id, competitor=None):
        user = super(CustomUpdateUserForm, self).save(commit=True)
        access_level = AccessLevel.objects.get(level=level_id)
        try:
            profile = Profile.objects.get(user=user)
            profile.access_level = access_level
            profile.save()
            if competitor:
                competitor = Competitors.objects.get(pk=competitor)
                profile.competitor = competitor
                profile.save()
            else:
                profile.competitor = None
                profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, access_level=access_level)
        return user
