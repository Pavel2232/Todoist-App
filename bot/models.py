from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

import os

from django.db import models

from core.models import User


# Create your models here.
class TgUser(models.Model):
    chat_id = models.CharField(max_length=255,unique=True)
    username = models.CharField(max_length=255,null=True,blank=True,default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    verification_code = models.CharField(max_length=32,null=True,blank=True,default=None)


    @staticmethod
    def _get_verification_code() -> str:
        return os.urandom(12).hex()


    def set_verification_code(self) -> str:
        self.verification_code = self._get_verification_code()
        self.save(update_fields=('verification_code', ))

        return self.verification_code