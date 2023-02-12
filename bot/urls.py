from django.urls import path

from bot.views import VeryficationView

urlpatterns = [
      path('verify', VeryficationView.as_view()),
]