from django.urls import path, include

from . import views

urlpatterns = [
    path(r'', views.connection_handler)
]