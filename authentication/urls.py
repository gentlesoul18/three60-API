from django.urls import path
from .views import LoginView, VerifyEmailView


urlpatterns = [
    #path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('signin',LoginView.as_view(), name='signin')
]