from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from core.managers import UserManager
from django.db import models



class UserRoles(models.TextChoices):
    USER = 'user','User'
    ADMIN = 'admin','Admin'

class User(AbstractBaseUser):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)





    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []




    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
