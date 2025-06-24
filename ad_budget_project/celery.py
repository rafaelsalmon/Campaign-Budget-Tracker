
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ad_budget_project.settings")
app = Celery("ad_budget_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
