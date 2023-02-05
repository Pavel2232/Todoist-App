from django.urls import path
from core.views import SingupView,LoginUserView

urlpatterns = [
      path('signup', SingupView.as_view()),
      path('login', LoginUserView.as_view()),
]