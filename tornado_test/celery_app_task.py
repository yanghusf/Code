import celery
import time

backend: str = 'redis://192.168.41.104:6379/1'
broker: str = "redis://192.168.41.104:6379/2"

cel:celery.Celery = celery.Celery("test", backend=backend, broker=broker)
@cel.task
def add(x, y):
    return x + y



