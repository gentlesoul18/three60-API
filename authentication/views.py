from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from three60.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin
from three60.utils import send_mail

from authentication.services import user_get_or_create, google_get_access_token, google_validate_id_token, google_get_user_info, jwt_login
from authentication.selectors import get_user
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.models import User

from urllib.parse import urlencode

import jwt,datetime

# Create your views here.

class RegisterView(GenericAPIView, ApiAuthMixin):
    serializer_class = RegisterSerializer

    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email= user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        print(current_site)
        relative_url = reverse('verify-email')
        absolute_url  = "http://" + current_site + relative_url + "?token=" + str(token)
        body = f"Hi {user.username}, verify your email with  this link \n {absolute_url}"
        subject = 'email verification'
        from_mail = 'devgentlesoul18@gmail.com'

        data = {'email_subject':subject, 'email_body':body, 'from_email':from_mail, 'to_email':[user.email]}

        send_mail(data)

    
        return Response({'data':user_data, 'success':'verification link have been sent to your email'}, status= status.HTTP_201_CREATED)


class VerifyEmailView(GenericAPIView):
    swagger_schema = None
    def get(self, request):
        token =request.GET.get('token')



        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(redirect(f'{settings.BASE_FRONTEND_URL}\login'))

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'timeout':'token has expired'}
            )

        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'error':'invalid token'}
            )
            

class LoginView(GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=username)

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        # payload = {
        #     "id": user.id,
        #     "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        #     "iat": datetime.datetime.utcnow(),
        # }

        #token = jwt.encode(payload, "secret", algorithm="HS256") # generates access token for login
        serializer = UserSerializer(user)

        response = Response()
        # token = user.tokens()
        # response.set_cookie(key="jwt", value=token.access_token, httponly=True) # creates cookies for user session
        response.data = {"tokens": user.tokens(), "data":serializer.data}
        return response


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
    swagger_schema = None
    def get(self, request):
        return Response(get_user(user=request.user))


class UserInitApi(PublicApiMixin, ApiErrorsMixin, APIView):
    swagger_schema = None
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
