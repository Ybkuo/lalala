#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-09 16:27:53
# @Author  : Ybkuo (1295055727@qq.com)
# @Version : $2.0$
# 利用多线程抓取西刺代理上一些可用的IP，建立IP代理池

import threading
import requests
import random
import queue
import re
import time

info_queue = queue.Queue()
ip_queue = queue.Queue()

headers_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 \
    Firefox/61.0',
    'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
    'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR \
    3.0.04506.30)',
    'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, \
    like Gecko) Chrome/3.0.195.33 Safari/532.0',
    'Mozilla/4.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, \
    like Gecko) Chrome/1.0.154.59 Safari/525.19',
    'Mozilla/4.0 (compatible; MSIE 6.0; Linux i686 ; en) Opera 9.70',
    'Mozilla/4.0 (compatible; MSIE 6.0; Mac_PowerPC; en) Opera 9.24',
]
headers = {"User-Agent": random.choice(headers_list)}


class get_ip_info(threading.Thread):
    """docstring for get_ip_info"""

    def __init__(self, page, info_queue):
        super(get_ip_info, self).__init__()
        self.page = page
        self.info_queue = info_queue

    # 抓取IP代理信息
    def run(self):
        html = ''
        s = requests.session()
        for i in range(1, self.page):
            url = 'http://www.xicidaili.com/nn/' + str(i)
            r = s.get(url, headers=headers)
            html += r.content.decode('utf-8')
        urlpat1 = '<td>(\d+\.\d+\.\d+\.\d+).*?<td>(\d+)</td>.*?'
        urlpat2 = '<td>(HTTP\w?)</td>.*?<div class="bar_inner (\w+)".*?>'
        urlpat = urlpat1+urlpat2
        result = re.compile(urlpat, re.S).findall(html)
        result.append('END')
        # 把IP信息写入队列
        for a in result:
            self.info_queue.put(a)
            self.info_queue.task_done()
        print("info_queue入队 ", self.info_queue.empty())


class proxy_ip(threading.Thread):
    """docstring for proxy_ip"""

    def __init__(self, info_queue, ip_queue):
        super(proxy_ip, self).__init__()
        self.info_queue = info_queue
        self.ip_queue = ip_queue

    # 建立IP代理池
    def run(self):
        # ip_info = get_ip_info(url)
        print("info_queue准备出队 ", self.info_queue.empty())
        while True:
            i = self.info_queue.get()
            if i == 'END':
                break
            else:
                if i[3] == 'fast':
                    proxies = {}
                    keys = i[2]
                    ip = 'http://' + i[0] + ':' + i[1]
                    proxies[keys] = ip
                    self.ip_queue.put(proxies)
                    self.ip_queue.task_done()
                else:
                    pass
        self.ip_queue.put('END')
        self.ip_queue.task_done()
        print("info_queue出队 ", self.info_queue.empty())
        print("ip_queue入队 ", self.ip_queue.empty())


class check_ip(threading.Thread):
    """docstring for check_ip"""

    def __init__(self, ip_queue):
        super(check_ip, self).__init__()
        self.ip_queue = ip_queue

    # 检测IP是否存活,返回新的IP代理池
    def run(self):
        new_proxy = []
        print("ip_queue准备出队 ", self.ip_queue.empty())
        while True:
            i = self.ip_queue.get()
            if i == 'END':
                break
            else:
                try:
                    requests.get(
                        'http://www.baidu.com',
                        headers=headers,
                        proxies=i,
                        timeout=5)
                    new_proxy.append(i)
                except TimeoutError:
                    pass
        print("ip_queue出队 ", self.ip_queue.empty())
        print(new_proxy)
        return new_proxy


# 定义爬取的页数，验证存活IP个数
if __name__ == '__main__':
    a = time.time()
    t1 = get_ip_info(2, info_queue)
    t1.start()
    t2 = proxy_ip(info_queue, ip_queue)
    t2.start()
    t3 = check_ip(ip_queue)
    t3.start()
    print(time.time()-a)
