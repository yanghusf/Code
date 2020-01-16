from celery.result import AsyncResult
from tasks import app

asc = AsyncResult(id="829accff-29b2-44f4-92ce-d6f724dd372c", app=app)
if asc.successful():
    result = asc.get()
    print(result)
elif asc.failed():
    print("执行失败")
elif asc.status =="PENDING":
    pass
elif asc.status == "RETRY":
    print("任务异常后正在重试")
elif asc.status == "STARTED":
    print("任务已经开始被执行")