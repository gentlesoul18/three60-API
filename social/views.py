from urllib.parse import urlencode
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from api.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin
from authentication.services import user_create, user_create_superuser, user_get_or_create, user_record_login, user_change_secret_key
from authentication.selectors import get_user
from social.services import google_get_access_token, google_validate_id_token, google_get_user_info, jwt_login

class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        domain = get_current_site(request).domain
        api_uri = reverse('google-login')
        redirect_uri = f'{domain}{api_uri}'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('givenName', ''),
            'last_name': user_data.get('familyName', ''),
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**profile_data)

        response = redirect(settings.BASE_FRONTEND_URL)
        response = jwt_login(response=response, user=user)

        return response


class UserApi(ApiAuthMixin, ApiErrorsMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response(get_user(user=request.user))


class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        first_name = serializers.CharField(required=False, default='')
        last_name = serializers.CharField(required=False, default='')

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get('Authorization')
        google_validate_id_token(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        response = Response(data=get_user(user=user))
        response = jwt_login(response=response, user=user)

        return response
