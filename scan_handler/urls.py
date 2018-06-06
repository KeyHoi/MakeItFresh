from django.urls import re_path

from . views import get_scanner_template

urlpatterns = [
    re_path(r'', get_scanner_template),
]
