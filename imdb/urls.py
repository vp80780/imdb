"""imdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
#from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from django.conf.urls import url, include
from apps.accounts.views import CreateEmailUserViewSet, obtain_auth_token
from apps.movies.views import AdminMoviesViewset, UserMoviesViewset


router = routers.DefaultRouter()
router.register('create-user', CreateEmailUserViewSet, base_name='create-user')
router.register('admin-movies', AdminMoviesViewset, base_name='admin-movies')
router.register('movies', UserMoviesViewset, base_name='movies')


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', obtain_auth_token),
]
