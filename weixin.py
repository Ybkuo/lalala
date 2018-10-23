#!/usr/bin/env python
# coding=utf-8

import re
import os
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20\
    100101 Firefox/61.0'
}


def info(url):
    info_list = []
    s = requests.session()
    r = s.get(url, headers=headers)
    html = r.content.decode('utf-8')
    urlpat = '<h3>.*?href="(http://\S*?)".*?>(.*?)</a>.*?<a.*?id="sogou_vr_11002601_account_\d+".*?>(.*?)</a>.*?<script>.*?(\d+).*?</span>'
    result = re.compile(urlpat, re.S).findall(html)
    # print(result)
    for info in result:
        info_list_l = list(info)
        info_url = info_list_l[0].replace('amp;', '')
        info_header = info_list_l[1].replace(
            '<em><!--red_beg-->', '').replace('<!--red_end--></em>', '').replace('&mdash;', '')
        info_writer = info_list_l[2]
        info_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(int(info_list_l[3])))
        info_list_l[0] = info_url
        info_headerpat = '[\*<>\|\?\\/:\"]'
        info_list_l[1] = re.sub(info_headerpat, '-', info_header)
        info_list_l[2] = info_writer
        info_list_l[3] = info_time
        info_list.append(info_list_l)
    return info_list


def article(url, page):
    s = requests.session()
    info_list = info(url)
    for i in info_list:
        path = 'php代码审计/' + i[1] + '-' + i[2] + '.html'
        html1 = '''<!doctype html>
		<html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0,viewport-fit=cover">
		<meta name="apple-mobile-web-app-capable" content="yes">
		<meta name="apple-mobile-web-app-status-bar-style" content="black">
		<meta name="format-detection" content="telephone=no">
		<title></title>
		</head>
		<body>
		'''
        r = s.get(i[0], headers=headers)
        html = r.content.decode('utf-8')
        contentpat = 'id="js_content".*?>(.*)id="js_toobar3"'
        content = re.compile(contentpat, re.S).findall(html)
        result = html1 + '<p>标题：' + i[1] + '</p><p>作者：' + i[2] + \
            '</p><p>时间：' + i[3] + '</p><p>内容：' + str(content) + '</p></br>'
        data = result.replace('\n', '')
        try:
            with open(path, "wb") as f:
                f.write(data.encode("utf-8"))
            print(path)
        except Exception as a:
            print(a)
            os.system('mkdir php代码审计')


url = 'http://weixin.sogou.com/weixin?oq=&query=\
php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input\
&ri=0&_sug_=n&type=2&sst0=1533624058715&page=1&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
article(url, 1)
