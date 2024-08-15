#!/usr/bin/env python3
# coding: utf-8

import threading
import time
import datetime

class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._flag = threading.Event()     # 用于暂停线程的标识
        self._flag.set()       # 设置为True
        self._running = threading.Event()      # 用于停止线程的标识
        self._running.set()      # 将running设置为True

    def run(self):
        while self._running.is_set():
            self._flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            # print(time.time())
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            time.sleep(0.1)

    def pause(self):
        self._flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self._flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        # self.__flag.set()       # 确保线程为非暂停状态
        self._running.clear()        # 将running设置为 False
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + '-------- stop --------')


if __name__ == '__main__':
    job = Job()
    job.start()
    time.sleep(1) # 线程运行1秒后暂停
    job.pause()

    time.sleep(3)  # 线程暂停3秒后继续打印时间戳
    job.resume()

    time.sleep(3)  # 线程运行3秒后暂停
    job.pause()

    time.sleep(2)  # 2秒后停止
    job.stop()
