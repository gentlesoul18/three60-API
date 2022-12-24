from rest_framework import serializers
from three60.utils import PlainValidationError
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            )
    username = serializers.CharField(
            required=True,
            )
    password = serializers.CharField(write_only=True, required=True,)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username',  'email', 'password', 'confirm_password']
        extra_kwargs = {
            'email':{'unique':True},
            'username':{'unique': True},
        }


    def validate(self, attrs):
        """
        checks if parameters passed in are valid
        e.g Password length, email uniqueness, et.c
        
        """
        
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise PlainValidationError({"username":"This username exist, please enter a new username"})
        elif email_exists:
            raise PlainValidationError({"email":"This email exist, please enter a new email"})
        elif len(attrs['password']) < 8:
            raise PlainValidationError({"password": "Password to short, it must contain atleast 8 characters!"})
        elif attrs['password'] != attrs['confirm_password']:
            raise PlainValidationError({"password":"Password fields doesn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'], 
            email=validated_data['email']
        )

        
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

