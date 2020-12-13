import threading
import time

def func1():
    for i in range(8):
        e.wait()
        time.sleep(1)
        print('a')

def func2():
    for i in range(14):
        e.clear()
        time.sleep(2)
        print('b')
        e.set()

e = threading.Event()
x=threading.Thread(target=func1, args=())
x.start()
y=threading.Thread(target=func2, args=())
y.start()


x.join()
y.join()