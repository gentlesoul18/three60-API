from django.urls import path
from .views import LoginView, RegisterView, GoogleLoginApi, UserApi, UserInitApi


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('signin',LoginView.as_view(), name='signin'),
    path('google-login/', GoogleLoginApi.as_view(),name='google-login' ),
    path('user/', UserApi.as_view(), name='user'),
    path('init/', UserInitApi.as_view(), name='init'),
]
