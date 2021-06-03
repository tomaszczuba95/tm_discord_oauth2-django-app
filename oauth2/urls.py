"""oauth2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from tmdiscordcauth import views
from rest_framework import routers
from tmdiscordcauth.views import TrackmaniaUserViewSet

router = routers.DefaultRouter()
router.register(r'api', TrackmaniaUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/user', views.get_authenticated_user,
         name='get_authenticated_user'),
    path('', views.discord_login, name="oauth_discord_login"),
    path('oauth2/logintm', views.trackmania_login, name="oauth_tm_login"),
    path('oauth2/login/redirect',
         views.discord_login_redirect, name="discord_redirect"),
    path('oauth2/logintm/redirect',
         views.trackmania_login_redirected, name="tm_redirect"),
    path('', include(router.urls)),
]
