"""
WSGI config for make_it_fresh_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from scan_handler import models

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'make_it_fresh_2.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "make_it_fresh_2.settings")

application = get_wsgi_application()
"""
proc = subprocess.Popen(
    ['/home/keyhoi/Uni/SS18/Business_Plan_Advanced_Seminar/make_it_fresh_2/env/bin/python3',
     '/home/keyhoi/Uni/SS18/Business_Plan_Advanced_Seminar/make_it_fresh_2/scan_handler/get_receipt_from_barcode.py',
     '4029764444956'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    env={'PYTHONPATH': os.pathsep.join(sys.path), 'DJANGO_SETTINGS_MODULE': 'make_it_fresh_2.settings'})
print("Subprocess finished with output: \n {}".format(proc.communicate()[0]))
"""
