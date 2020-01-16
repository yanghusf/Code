import threading
import time
def sing():
    for i in range(5):
        print(f"正在唱歌中{i}")
        time.sleep(1)

if __name__ == '__main__':
    for i in range(5):
        t = threading.Thread(target=sing)
        t.start()

    while True:
        current_len = len(threading.enumerate())
        print(f"当前线程数量{current_len}")