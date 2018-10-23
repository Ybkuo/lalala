#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-08 11:31:14
# @Author  : Ybkuo (1295055727@qq.com)
# @Version : $1.0$

import queue
import threading

arg = queue.Queue()


class test1(threading.Thread):
        """docstring for test1"""
        def __init__(self, arg):
                super(test1, self).__init__()
                self.arg = arg

        def run(self):
                for i in range(100):
                        self.arg.put(i)
                        # self.arg.task_done()


class test2(threading.Thread):
        """docstring for test2"""
        def __init__(self, arg):
                super(test2, self).__init__()
                self.arg = arg

        def run(self):
                while not self.arg.empty():
                        print(self.arg.get())


t1 = test1(arg)
t1.start()
t2 = test2(arg)
t2.start()
