from django.contrib import admin

from bot.models import TgUser

# Register your models here.
admin.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    ...