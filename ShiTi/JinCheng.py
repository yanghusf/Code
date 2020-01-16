from multiprocessing import Process

import time
def foo():
    print('守护进程开始')
    time.sleep(5)
    print('守护进程结束')
def task():
    print('子进程开始')
    time.sleep(3)
    print('子进程开始')

if __name__ == '__main__':
    p1 = Process(target=foo)
    p2 = Process(target=task)
    p1.daemon = True # 一定要凡在start 之前
    p1.start()
    p2.start()
    # p2 = Process(target=task)
    print('主进程')