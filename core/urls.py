from django.urls import path
from core.views import SingupView, LoginUserView, GetEditProfile, UpdatePasswordView

urlpatterns = [
    path('signup', SingupView.as_view()),
    path('login', LoginUserView.as_view()),
    path('profile', GetEditProfile.as_view()),
    path('update_password', UpdatePasswordView.as_view()),
]
