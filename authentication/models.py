from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Create your models here.

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)


    
    
    REQUIRED_FIELDS = []
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        access = AccessToken.for_user(self)
        return {'access':str(access), 'refresh':str(refresh)}