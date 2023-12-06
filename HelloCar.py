import time
import threading


def worker(name):
    for i in range(5):
        print(name, i)
        time.sleep(0.5)


t1 = threading.Thread(target=worker, args=('计数器A',))
t1.start()
t2 = threading.Thread(target=worker, args=('计数器B',))
t2.start()
print('完成')
