from django.urls import path
from .views import GoogleLoginApi, UserApi, UserInitApi

urlpatterns = [
    path('google-login/', GoogleLoginApi.as_view(),name='google-login' ),
    path('user/', UserApi.as_view(), name='user'),
    path('init/', UserInitApi.as_view(), name='init'),
]