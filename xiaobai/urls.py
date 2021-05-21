"""xiaobai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from front import views as front_views
from cms import views as cms_views

urlpatterns = [
    path('', front_views.index,name='index'),
    path('signup/', front_views.signup,name='signup'),
    path('signin/', front_views.signin,name='signin'),
    path('logout/', front_views.logout,name='logout'),
    path('profile/', front_views.profile,name='profile'),
    path('upload/', front_views.upload_avatar,name='upload_avatar'),
    path('upload_certificate/', front_views.upload_certificate,name='upload_certificate'),
    path('repwd/', front_views.repwd,name='repwd'),
    path('settings/', front_views.settings,name='settings'),
    path('pub_offer/', front_views.pub_offer,name='pub_offer'),
    path('cms/signin/', cms_views.signin,name='cms_signin'),
    path('cms/logout/', cms_views.logout,name='cms_logout'),
    path('cms/', cms_views.index,name='cms_index'),
    path('cms/banner/', cms_views.banner,name='cms_banner'),
    path('cms/upload_banner/', cms_views.upload_banner, name='upload_banner'),
    path('cms/edit_banner/', cms_views.edit_banner, name='edit_banner'),
    path('cms/delete_banner/', cms_views.delete_banner, name='delete_banner'),
    path('cms/user/', cms_views.user_manage, name='user_manage'),
    path('cms/banned/', cms_views.banned_user, name='banned_user'),
    path('cms/liftbanned/', cms_views.liftbanned_user, name='liftbanned_user'),
    path('cms/job/', cms_views.job_type, name='job_type'),
    path('cms/add_jobtype/', cms_views.add_jobtype, name='add_jobtype'),
    path('cms/edit_jobtype/', cms_views.edit_jobtype, name='edit_jobtype'),
    path('cms/delete_jobtype/', cms_views.delete_jobtype, name='delete_jobtype'),
]
