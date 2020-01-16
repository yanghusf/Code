from celery import Celery
from datetime import timedelta
from celery.schedules import crontab



app = Celery("tasks")
app.config_from_object('test_celery.celeryconfig')

