from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')

app = Celery('eCommerce')


app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Tehran')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"request: {self.request!r}")
    
