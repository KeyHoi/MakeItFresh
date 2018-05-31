from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^', views.connection_handler),
    re_path(r'(?P<mode>\w+)&(?P<token>\w+)&(?P<challenge>\w+)', views.http_get_handler)
]