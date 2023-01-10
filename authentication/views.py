from os import access
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from django.db.models import Q

from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from three60.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin
from three60.utils import send_mail

from authentication.services import (
    user_get_or_create,
    google_get_access_token,
    google_validate_id_token,
    google_get_user_info,
    jwt_login,
)
from authentication.selectors import get_user
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.models import User


from urllib.parse import urlencode

import jwt, datetime

# Create your views here.


class RegisterView(GenericAPIView, ApiAuthMixin):
    """
    View to sign up new user using normal registration
    """

    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = user.tokens()
        response = Response()
        response.data = {**user_data, "access_token": token}
        return response


class LoginView(GenericAPIView):
    """
    View to Log in Existing Users
    """

    serializer_class = UserSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except BaseException as e:
            raise ValidationError({"message": "This user does not exist"})

        if not user.check_password(password):
            raise ValidationError({"message": "Incorrect Password!"})

        serializer = UserSerializer(user)

        response = Response()
        token = user.tokens()
        response.set_cookie(
            key="jwt", value=token, httponly=True
        )  # creates cookies for user session
        response.data = {"access_token": token, **serializer.data}
        return response


class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    """
    Google Login View to log user in with just a click
    parameter needed: code sent to google from frontend
    The code is used to generate users access token then the access token,
    the access token is then used to generate the user's data from google
    """

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        
    serializer_class = InputSerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="code",
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ]
    )

    

    def post(self, request):

        code = request.GET.get('code')
    
    
        # code = request.data['code']

        user_data = google_get_user_info(access_token=code)

        profile_data = {
            "email": user_data["email"],
            "username": user_data.get("given_name", ""),
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.

        print (profile_data)
        user, _ = user_get_or_create(**profile_data)

        response = Response()
        response = jwt_login(response=response, user=user)

        return response


# class UserApi(ApiAuthMixin, ApiErrorsMixin, APIView):
#     swagger_schema = None

#     def get(self, request):
#         return Response(get_user(user=request.user))


# class CreateUserApi(PublicApiMixin, ApiErrorsMixin, APIView):
#     """
#     This view is used to create user that logs in with google
#     the user's info is added to the apps database
#     """

#     swagger_schema = None

#     class InputSerializer(serializers.Serializer):
#         email = serializers.EmailField()
#         username = serializers.CharField(required=False, default="")

#     @swagger_auto_schema(request_body=InputSerializer)
#     def post(self, request, *args, **kwargs):
#         id_token = request.headers.get("Authorization")
#         google_validate_id_token(id_token=id_token)

#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # We use get-or-create logic here for the sake of the example.
#         # We don't have a sign-up flow.
#         user, _ = user_get_or_create(**serializer.validated_data)

#         response = Response(data=get_user(user=user))
#         response = jwt_login(response=response, user=user)

#         return response
