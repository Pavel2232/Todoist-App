from django.contrib.auth import  authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import authentication, exceptions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from core.models import User
from core.serializers import SingupUserSerializer, LoginUserSerializer


# Create your views here.

class SingupView(CreateAPIView):
    serializer_class = SingupUserSerializer


class DjangoAuthBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return None

        user = authenticate(username=username, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username or password')

        login(request, user)
        return (user, None)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
class LoginUserView(CreateAPIView):
    serializer_class = LoginUserSerializer
    # authentication_classes = (DjangoAuthBackend,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        login(request = self.request, user = serializer.save())
