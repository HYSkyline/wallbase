# -*- coding:utf-8 -*-

from __future__ import division
import time
import threading
import os


def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


def loop(count):
    t0 = now()
    print 'thread %s is running...' % threading.current_thread().name + "\ttime:" + t0
    n = 0
    while n < 10:
        n += 1
        print 'thread %s >>> %s, %s' % (threading.current_thread().name, n, count)
        time.sleep(0.4)
    print 'thread %s ended.' % threading.current_thread().name


def aim():
    t00 = now()
    print 'thread %s is running...' % threading.current_thread().name + "\ttime:" + t00
    count = 990
    while count < 1000:
        count += 1
        print 'thread %s >>> %s' % (threading.current_thread().name, count)
        time.sleep(0.3)
    print 'thread %s ended.' % threading.current_thread().name


t0 = now()
print 'thread %s is running...\n' % threading.current_thread().name + t0
threadpool = []
count = 'f'
for i in range(0, 2):
    th = threading.Thread(target=loop,args=(count))
    threadpool.append(th)
for th in threadpool:
    th.start()
for th in threadpool:
    threading.Thread.join(th)
t0 = now()
print 'All sub_threads finished.' + t0
os.system('pause')
t0 = now()
print 'thread %s ended.' % threading.current_thread().name + t0




# j = '>'
# if __name__ == '__main__':
#     for i in range(1, 61):
#         j += '>'
#         sys.stdout.write(j+'  '+str(int((i/60)*100))+"\r")
#         sys.stdout.flush()
#         time.sleep(0.2)
# print
