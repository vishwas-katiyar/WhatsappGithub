"""Whatsapp_Analyser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from Whatsapp_Analyser_App import views

from django.views.static import serve
from django.conf.urls import url
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index' ),
    path('features/',views.features,name='features' ),
    path('users/',views.users,name='users' ),
    path('bot/',views.bot,name='bot' ),
]
