"""pydk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from common import views as common_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact_info/', common_views.ContactInfoView.as_view(), name='contact_info'),
    path('about_me/', common_views.AboutMeView.as_view(), name='about_me'),
    path('martor/', include('martor.urls')),
    path('', include('blog.urls', namespace='blog')),
]
