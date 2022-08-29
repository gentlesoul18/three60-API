from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model, hashers
from .models import User
from .serializers import UserSerializer


serializer = UserSerializer
class UsernameOrEmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return 
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User.set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
    
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

# from django.contrib.auth.hashers import check_password
# from django.contrib.auth import get_user_model
# from django.conf import settings

# from django.db.models import Q

# from rest_framework_simplejwt.exceptions import AuthenticationFailed
# from .serializers import UserSerializer

# User = settings.AUTH_USER_MODEL


# class EmailorUsernameAuthenticationBackend(object):
#     def authenticate(self, request, username=None, password=None):
#         if '@' in username:
#             kwargs = {'email':username}
#         else:
#             kwargs = {}
#         try:
#             serializer = UserSerializer(User)
#             username = serializer.data['username']
#             print(username)
#             user = User.objects.filter(
#                 Q(username=username) | Q(email=username)
#             )
#             if not user and check_password(password, user.password):
#                 raise AuthenticationFailed("wrong username or password")

#             return user


#         except User.DoesNotExist:
#             return None

        
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None