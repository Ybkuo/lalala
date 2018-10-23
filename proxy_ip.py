#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-08 11:38:13
# @Author  : Ybkuo (1295055727@qq.com)
# @Version : $1.0$
# 抓取西刺代理上一些可用的IP，建立IP代理池

import requests
import random
import re

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


# 抓取IP代理信息
def get_ip_info(page):
    html = ''
    s = requests.session()
    for i in range(1, page):
        url = 'http://www.xicidaili.com/nn/' + str(i)
        r = s.get(url, headers=headers)
        html += r.content.decode('utf-8')
    urlpat = '<td>(\d+\.\d+\.\d+\.\d+)</td>.*?<td>(\d+)</td>.*?<td>(HTTP\w?)\
    </td>.*?<div class="bar_inner (\w+)".*?>'
    result = re.compile(urlpat, re.S).findall(html)
    # print(result)
    return result


# 建立IP代理池
def proxy_ip(ip_info):
    proxy = []
    # ip_info = get_ip_info(url)
    for info in ip_info:
        if info[3] == 'fast':
            proxies = {}
            keys = info[2]
            ip = 'http://' + info[0] + ':' + info[1]
            proxies[keys] = ip
            proxy.append(proxies)
        else:
            pass
    return proxy


# 检测IP是否存活,返回新的IP代理池
def check_ip(page):
    new_proxy = []
    proxy_ip_list = proxy_ip(get_ip_info(page))
    for proxies in proxy_ip_list:
        if len(new_proxy) <= Proxy_num:
            try:
                requests.get(
                    "http://www.baidu.com",
                    headers=headers,
                    proxies=proxies,
                    timeout=5)
                new_proxy.append(proxies)
            except TimeoutError:
                pass
        else:
            pass
    return new_proxy


# 定义爬取的页数，验证存活IP个数
if __name__ == '__main__':
    Proxy_num = 10
    print(check_ip(2))
