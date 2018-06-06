from django.urls import re_path

from . views import get_receipt_template

urlpatterns = [
    re_path(r'', get_receipt_template),
]
