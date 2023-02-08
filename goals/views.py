from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter, CommentGoalFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, Status, GoalComment, Board
from goals.permissions import BoardPermissions, BoardUserPermission, GoalBoardUserPermission, CommentBoardUserPermission
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalGoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer, BoardSerializer, BoardCreateSerializer, BoardListSerializer


# Create your views here.
"""Вьюхи Категорий целей """
class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated,BoardUserPermission]

class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated,]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created",'board']
    ordering = ["title"]
    search_fields = ["title"]
    filterset_fields = ['board']
    filterset_class = GoalCategoryFilter

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False,
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated,BoardUserPermission]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.goals_category.update(status=Status.archived)
        instance.save()
        return instance



class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalGoalCreateSerializer
    permission_classes = [IsAuthenticated,GoalBoardUserPermission]


"""Вьюхи целей"""
class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated,]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created",'due_data','priority']
    ordering = ["created"]
    search_fields = ["title",'description']
    filterset_class = GoalDateFilter


    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user,
             status= Status.to_do or Status.done or Status.in_progress
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated,GoalBoardUserPermission]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            status= Status.to_do or Status.done or Status.in_progress
        )

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance

"""Вьюхи коментариев"""
class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated,]


class CommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated,]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ['goal']
    ordering = ["-created",'update']
    filterset_class = CommentGoalFilter


    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,CommentBoardUserPermission]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)

"""Вьюхи досок"""
class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering = ["title"]
    search_fields = ["title"]


    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived
            )
        return instance


class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated,]




class BoardListView(ListAPIView):
    model = Board
    permission_classes = [IsAuthenticated,BoardPermissions]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering = ["title"]
    search_fields = ["title"]


    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
