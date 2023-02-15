from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment

"""Ограничения для досок,целей,комментариев и вывод их пользователю"""


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class BoardUserPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(
                user=request.user).exists()
        return GoalCategory.objects.filter(
            board__participants__user=request.user, board__participants__role=BoardParticipant.Role.writer.owner
        ).exists()


class GoalBoardUserPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return Goal.objects.filter(
                user=request.user).exists()
        return Goal.objects.filter(
            category__board__participants__user=request.user,
            category__board__participants__role=BoardParticipant.Role.writer.owner
        ).exists()


class CommentBoardUserPermission(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return GoalComment.objects.filter(
                user=request.user).exists()
        return GoalComment.objects.filter(
            goal__category__board__participants__user=request.user,
            goal__category__board__participants__role=BoardParticipant.Role.writer.owner
        ).exists()
