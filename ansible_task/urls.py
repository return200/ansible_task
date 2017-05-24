"""ansible_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^$', views.defaultview),
    url(r'^admin/', admin.site.urls),
    url(r'^file/$', views.fileview),
    url(r'^shell/$', views.shellview),
    url(r'^copy/$', views.copyview),
    url(r'^software/$', views.softwareview),
    url(r'^service/$', views.serviceview),
    url(r'^crontab/$', views.crontabview),
]
