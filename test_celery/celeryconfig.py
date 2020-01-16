from celery.schedules import crontab
from datetime import timedelta

broker_url = 'redis://:newroot@192.168.80.128:6379/1'
result_backend = 'redis://:newroot@192.168.80.128:6379/2'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True

imports = [
    'test_celery.celery_tasks.tasks'
]

beat_schedule = {
    "get_result": {"task":"test_celery.celery_tasks.tasks.task1",
                   "schedule": timedelta(seconds=10),
                    'args': {}
                   },
    "results": {"task":"test_celery.celery_tasks.tasks.task2",
                   "schedule": timedelta(seconds=10),
                    'args': {}
                   }
}
