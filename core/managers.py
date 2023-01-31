from django.contrib.auth.models import (
    BaseUserManager
)

class UserManager(BaseUserManager):

    def create_user(self,username, email, first_name, last_name, phone, password=None,role = "user"):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username = username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username,email, first_name, last_name, phone, password=None,role = 'admin',):
        """
        функция для создания суперпользователя — с ее помощью мы создаем админинстратора
        это можно сделать с помощью команды createsuperuser
        """

        user = self.create_user(
            username = username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )
        user.is_superuser=True
        user.is_staff = True
        user.save(using=self._db)
        return user
