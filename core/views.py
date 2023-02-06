from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import authentication, exceptions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    get_object_or_404, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from core.models import User
from core.serializers import SingupUserSerializer, LoginUserSerializer, EditProfileSerializer, UptadePasswordSerializer


# Create your views here.

class SingupView(CreateAPIView):
    serializer_class = SingupUserSerializer



class LoginUserView(CreateAPIView):
    serializer_class = LoginUserSerializer


    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError({'username or password':"Неверный"})



class GetEditProfile(RetrieveUpdateDestroyAPIView):
    queryset = User
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated,]


    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Update_passwordView(UpdateAPIView):
    queryset = User
    serializer_class = UptadePasswordSerializer
    permission_classes = [IsAuthenticated,]

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
        return Response({"Пароль":"неверный"})


