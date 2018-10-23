#!/usr/bin/env python
# coding=utf-8

import requests
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20\
    100101 Firefox/61.0'
}


def dili_url(url):
    urllist = []
    s = requests.session()
    r = s.get(url, headers=headers)
    html = r.content.decode('utf-8')
    urllistpat = '<a href="(http://moe.005.tv/\d+\.html)" target="_blank"'
    urllist = re.compile(urllistpat, re.S).findall(html)
    # for i in result:
    # 	urll = 'http://moe.005.tv/'+i+'.html'
    # 	urllist.append(urll)
    return urllist


def dili_image(url, page):
    a = 1
    b = 1
    s = requests.session()
    urllist = dili_url(url)
    print(urllist)
    for i in urllist:
        r = s.get(i, headers=headers)
        html = r.content.decode('utf-8')
        urlpat = 'src="(\S*?\.jpg)"'
        image_url_list = re.compile(urlpat, re.S).findall(html)
        for x in image_url_list:
            img = requests.get(x).content
            path = "image/" + str(page) + "-" + str(a) + "-" + str(b) + ".jpg"
            try:
                with open(path, "wb") as f:
                    f.write(img)
            except Exception as a:
                print(a)
                os.system('mkdir image')
            print(path)
            b += 1
        a += 1


print('--------------------')
page_1 = input('起始页码：')
page_2 = input('结束页码：')
print('--------------------')
for i in range(int(page_1), int(page_2)):
    url = "http://moe.005.tv/moeimg/bz/list_4_" + str(page_1) + ".html"
    dili_image(url, page_1)
