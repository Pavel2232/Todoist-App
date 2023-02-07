from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


# Register your models here.
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "update")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "update")
    search_fields = ("title", "user")

class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "update")
    search_fields = ("text", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal,GoalAdmin)
admin.site.register(GoalComment,GoalCommentAdmin)