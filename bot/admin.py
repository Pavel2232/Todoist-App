from django.contrib import admin

from bot.models import TgUser

admin.register(TgUser)


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    ...
