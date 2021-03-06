"""make_it_fresh_2 URL Configuration

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
from django.http import HttpResponse
from django.urls import path, include

from scan_handler.views import get_receipt_template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scan_handler/', include('scan_handler.urls')),
    path(r'webhook/', include('facebook.urls')),
    path(r'distribute/', include('django_mobile_app_distribution.urls')),
    path(r'accounts/', include('django_mobile_app_distribution.auth_urls')),
    path(r'/receipts/<int:id>/', get_receipt_template)
]
