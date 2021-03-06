#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import time
import multiprocessing


# def worker():
#     print("start long job!")
#     time.sleep(15)
#     print("end long job!")
#
#
# p = multiprocessing.Process(target=worker)
# p.start()
#
# # try:
# #     print("start join!")
# #     p.join(5)
# #     print("join done!")
# # except multiprocessing.TimeoutError:
# #     print("timeout!")
# #     p.terminate()
#
# # 下面这段是正确的杀掉子进程的方法
# # 确认下queue会不会导致内存泄露
# p.join(5)
# if p.is_alive():
#     print("still alive! kill it!")
#     p.terminate()
#     p.join()

def child_worker():
    print("child worker start!")
    time.sleep(15)
    print("child worker stop!")


def parent_worker():
    print("parent worker start!")
    p = multiprocessing.Process(target=child_worker)
    p.start()
    p.join(5)
    if p.is_alive():
        p.terminate()
        p.join()
        print("kill confirmed!")
    print("parent worker stop!")


parent_process = multiprocessing.Process(target=parent_worker)
parent_process.start()
parent_process.join()

print("main done!")
while True:
    time.sleep(1)
