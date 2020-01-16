from .celery_c import app
import time
count = 0

@app.task
def task1(*args, **kwargs):
    global count
    count += 1
    time.sleep(2)
    return count
@app.task
def task2(*args, **kwargs):
    time.sleep(2)

    return time.time()




