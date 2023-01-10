from django.urls import path
from .views import LoginView, RegisterView, GoogleLoginApi ##, UserApi, CreateUserApi

app_name = 'authentication'

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("signin", LoginView.as_view(), name="signin"),
    path("google-login", GoogleLoginApi.as_view(), name="google-login"),
    # path("user/", UserApi.as_view(), name="user"),
    # path("create/", CreateUserApi.as_view(), name="create"),
]
