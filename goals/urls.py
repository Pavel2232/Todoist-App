from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalCreateView, GoalListView, \
    GoalView, CommentCreateView, CommentListView, CommentView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path('goal_category/<pk>', GoalCategoryView.as_view()),

    path('goal/create', GoalCreateView.as_view()),
    path('goal/list', GoalListView.as_view()),
    path('goal/<pk>', GoalView.as_view()),

    path('goal_comment/create', CommentCreateView.as_view()),
    path('goal_comment/list', CommentListView.as_view()),
    path('goal_comment/<pk>', CommentView.as_view()),
]