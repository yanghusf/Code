#!/usr/bin/env python
# -*- coding:utf-8 -*-
from celery_tasks import tasks

# 立即告知celery去执行xxxxxx任务，并传入两个参数
result = tasks.task1.delay(4, 4)

print(result.id)