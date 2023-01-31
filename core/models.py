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
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(max_length=255,unique=True)
    role = models.CharField(max_length=5,choices=UserRoles.choices)
    image = models.ImageField(upload_to='django_media/',null=True)
    is_active = models.BooleanField(default=True)
    groups = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'phone']

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER



    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
