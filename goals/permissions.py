from rest_framework import permissions

from goals.models import BoardParticipant, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()



class BoardUserPermission(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(
                user=request.user).exists()
        return GoalCategory.objects.filter(
            board__participants__user=request.user, board__participants__role= BoardParticipant.Role.writer or BoardParticipant.Role.owner
        ).exists()


class GoalBoardUserPermission(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(
                user=request.user).exists()
        return Goal.objects.filter(
            goals_category__board__participants__user=request.user, goals_category__board__participants__role= BoardParticipant.Role.writer or BoardParticipant.Role.owner
        ).exists()



class CommentBoardUserPermission(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return GoalComment.objects.filter(
                user=request.user).exists()
        return Goal.objects.filter(
            comments__goals_category__board__participants__user=request.user, comments__goals_category__board__participants__role= BoardParticipant.Role.writer or BoardParticipant.Role.owner
        ).exists()