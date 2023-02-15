from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import SingupUserSerializer, LoginUserSerializer, EditProfileSerializer, UptadePasswordSerializer


class SingupView(CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = SingupUserSerializer


class LoginUserView(CreateAPIView):
    """Вход в сервис"""
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'username or password': "Неверный"})


class GetEditProfile(RetrieveUpdateDestroyAPIView):
    """Детальная информация о пользователе"""
    queryset = User
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    """Вью для смены пароля"""
    queryset = User
    serializer_class = UptadePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        old_password = request.data.get('old_password')
        if request.user.check_password(old_password):
            serializer.instance.set_password(request.data.get('new_password'))
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({"Пароль": "неверный"})
