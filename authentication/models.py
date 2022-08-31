from cProfile import label
from os import access
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Create your models here.

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)


    
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        access = AccessToken.for_user(self)
        #returns access and rrefresh token of the user
        return {'refresh':str(refresh), 'access':str(access)}