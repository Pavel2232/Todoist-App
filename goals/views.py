from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter, CommentGoalFilter
from goals.models import GoalCategory, Goal, Status, GoalComment
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalGoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer


# Create your views here.
class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated,]

class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated,]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.goals_category.update(status=Status.archived)
        instance.save()
        return instance



class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalGoalCreateSerializer
    permission_classes = [IsAuthenticated,]



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
        return Goal.objects.filter(user=self.request.user,
             status= Status.to_do or Status.done or Status.in_progress
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user,
            status= Status.to_do or Status.done or Status.in_progress
        )

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance


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
        return GoalComment.objects.filter(user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return GoalComment.objects.filter(
            user=self.request.user)