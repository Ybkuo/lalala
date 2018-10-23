# ************************************************ #
# /usr/bin/env python                              #
# -*- coding: utf-8 -*-                            #
# aqgy.py                                          #
# By: Ybkuo <1295055727@qq.com>                    #
# Created: 2018/08/16 11:57:55 by Ybkuo            #
# Updated: 2018/08/16 11:57:55 by Ybkuo            #
# ************************************************ #
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


# 获取评论数据
def info(url):
    s = requests.session()
    r = s.get(url, headers=headers)
    html = r.content.decode('utf-8')
    avater_pat = 'comment-info.*?<a href="(.*?)".*?>(.*?)</a>'
    start_pat = '.*?allstar10 rating.*?title="(.*?)"'
    time_pat = '.*?comment-time.*?>.*?(\d+-\d+-\d+).*?</span>'
    text_pat = '.*?class="short">(.*?)</span>'
    infopat = avater_pat+start_pat+time_pat+text_pat
    result = re.compile(infopat, re.S).findall(html)
    print(result)


url = 'https://movie.douban.com/subject/24852545/comments?\
start=00&limit=20&sort=new_score&status=P'
info(url)
