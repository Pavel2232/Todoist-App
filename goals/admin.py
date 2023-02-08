from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board


# Register your models here.
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "update",'board')
    search_fields = ("title", "user",'board')


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "update")
    search_fields = ("title", "user")

class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "update")
    search_fields = ("text", "user")

class BoardAdmin(admin.ModelAdmin):
    list_display = ("title","created", "update")
    search_fields = ("title",)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal,GoalAdmin)
admin.site.register(GoalComment,GoalCommentAdmin)
admin.site.register(Board,BoardAdmin)