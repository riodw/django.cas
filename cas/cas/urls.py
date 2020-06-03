"""cas URL Configuration

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
# Custom
from django.conf.urls import url
from django.conf.urls import include
from .views import home, login_view, signup, loggedin, signin, oldkeys

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home),
    path('login/', login_view, name='cas_login'),
    path('signin/', signin),
    path('signup/', signup),
    path('oldkeys/', oldkeys),
    path('loggedin/', loggedin),
    url(r'', include('mama_cas.urls')),
]
