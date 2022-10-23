import os

from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreapp.settings')

app = Celery('coreapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
