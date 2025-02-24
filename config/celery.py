import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup() 


app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

from crawler.tasks import run_scraper