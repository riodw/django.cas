"""testapp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import django_cas_ng.views as cas_views
from django.conf.urls import url

urlpatterns = [
    # These urls are using an old format
    url(r'^accounts/login$', cas_views.login, name='cas_ng_login'),
    url(r'^accounts/logout$', cas_views.logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', cas_views.callback, name='cas_ng_proxy_callback'),
    path('admin/', admin.site.urls),
]
