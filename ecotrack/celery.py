import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecotrack.settings")

app = Celery("ecotrack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
