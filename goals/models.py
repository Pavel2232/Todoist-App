from django.db import models

from core.models import User


class BaseData(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    update = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class Board(BaseData):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(max_length=200, verbose_name="Название")
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


# Create your models here.
class GoalCategory(BaseData):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")

    def __str__(self):
        return self.title


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(BaseData):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name="Описание",max_length=1000, null=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT,
                                 related_name='goals_category')
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)
    due_date = models.DateTimeField(verbose_name="Крайний срок", blank=True, null=True)

    def __str__(self):
        return self.title


class GoalComment(BaseData):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.CharField(verbose_name="Комментарий",max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, related_name='comments_by_user')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE, related_name='comments')


class BoardParticipant(BaseData):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
