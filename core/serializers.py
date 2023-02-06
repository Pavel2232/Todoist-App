from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User



class SingupUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100,validators=[validate_password],write_only=True)
    password_repeat = serializers.CharField(max_length=100,write_only=True)




    class Meta:
        model = User
        fields = ['id','email','password','password_repeat','first_name','last_name','username']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user



class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['id','email','username','password','first_name','last_name']
        read_only_fields = ['id','email','first_name','last_name','username']



class EditProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id','email','username','first_name','last_name']
        read_only_fields = ['id']


class UptadePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=100,validators=[validate_password])
    old_password = serializers.CharField(max_length=100,write_only=True)

    class Meta:
        model = User
        fields = ['id','email','new_password','old_password','first_name','last_name','username']
        read_only_fields = ['id','email','first_name','last_name','username']



    def update(self, instance, validated_data):
        validated_data['new_password'] = make_password(validated_data['new_password'])
        return  super().update(instance,validated_data)


