from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

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


        def create(self,validated_data):
            if not (user := authenticate(
                    username=validated_data['username'],
                    password=validated_data['password'])
):
                raise AuthenticationFailed
            return user
