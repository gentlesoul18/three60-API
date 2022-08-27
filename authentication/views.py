
from operator import sub
from typing import Generic
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer
from .models import User
from .utils import send_mail

import jwt

# Create your views here.

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email= user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_url = reverse('verify-email')
        absolute_url  = "http://" + current_site + relative_url + "?token=" + str(token)
        body = f"Hi {user.username}, verify your email with  this link \n {absolute_url}"
        subject = 'email verification'
        from_mail = 'devgentlesoul18@gmail.com'

        data = {'email_subject':subject, 'email_body':body, 'from_email':from_mail, 'to_email':[user.email]}

        send_mail(data)

    
        return Response({'data':user_data, 'success':'verification link have been sent to your email'}, status= status.HTTP_201_CREATED)


class VerifyEmailView(GenericAPIView):
    def get(self, request):
        token =request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'success':'user successfully created'}, status=status.HTTP_202_ACCEPTED)

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
        pass