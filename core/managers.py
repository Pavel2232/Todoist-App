from django.contrib.auth.models import (
    BaseUserManager
)
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, first_name=None, last_name=None, password=None, password_repeat=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = True

        if password != password_repeat:
            raise ValidationError({'password_repeat': "Пароли не совпадают"})
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, first_name=None, last_name=None, password=None):
        """
        функция для создания суперпользователя — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
