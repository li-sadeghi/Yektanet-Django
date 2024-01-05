from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yektanet.settings')

app = Celery('Yektanet')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
