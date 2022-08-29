"""three60 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD:backend/three60/three60/urls.py
from social.views import GoogleLogin
=======
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="three60 API",
        default_version='1.0.0',
        description="API documentation of three60",
    ),
    public=True,
)
>>>>>>> e5b7de43d72a1ced4ba3379ee740d2644940ff31:three60/urls.py


urlpatterns = [
    path("admin/", admin.site.urls),
<<<<<<< HEAD:backend/three60/three60/urls.py

    path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('google/', GoogleLogin.as_view(), name='google-login'),
=======
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('social/', include('social.urls')),
>>>>>>> e5b7de43d72a1ced4ba3379ee740d2644940ff31:three60/urls.py
    path("api/auth/", include('authentication.urls')),

]
