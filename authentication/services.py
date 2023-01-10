from typing import Tuple, Dict, Any
from typing import Tuple
from django.core.management.utils import get_random_secret_key
from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import HttpResponse
from django.db import transaction
from rest_framework_simplejwt.tokens import AccessToken

from three60.utils import get_now, PlainValidationError

from authentication.models import User


import jwt, datetime, requests


GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
# to obtain the token to get user info
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
# GOOGLE_USER_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
# to obtain the user info with the token sent from google


def jwt_login(*, response: HttpResponse, user: User) -> HttpResponse:
    token = AccessToken.for_user(
        user
    )  # generates access token to authenticate user that logs in with google

    response.set_cookie(
        key="jwt", value=token, httponly=True
    )  # creates cookies for user session

    return response


def google_validate_id_token(*, id_token: str) -> bool:
    # Reference: https://developers.google.com/identity/sign-in/web/backend-auth#verify-the-integrity-of-the-id-token
    response = requests.get(GOOGLE_ID_TOKEN_INFO_URL, params={"id_token": id_token})

    if not response.ok:
        raise ValidationError("id_token is invalid.")

    audience = response.json()["aud"]

    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        raise ValidationError("Invalid audience.")

    return True


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        "code": code,
        "client_id": settings.GMAIL_API_CLIENT_ID,
        "client_secret": settings.GMAIL_API_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError("Failed to obtain access token from Google.")

    access_token = response.json()["access_token"]

    return access_token


def google_get_user_info(access_token: str):  # -> Dict[str, Any]
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(
        GOOGLE_USER_INFO_URL, params={"access_token": access_token, "alt": "json"}
    )

    if not response.ok:
        print(response.json())
        raise PlainValidationError(
            {"message": "Failed to obtain user info from Google."}
        )

    return response.json()


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

    user = user_create(email=email, password=password, **extra_fields)

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()
    # after querying user from database, if user exist, it return user
    if user:
        return user, False
    # else it creates the user with the info that we got from the user's mail
    return user_create(email=email, **extra_data), True
