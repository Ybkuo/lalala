# ************************************************ #
# /usr/bin/env python                              #
# -*- coding: utf-8 -*-                            #
# login.py                                         #
# By: Ybkuo <1295055727@qq.com>                    #
# Created: 2018/08/16 11:56:58 by Ybkuo            #
# Updated: 2018/08/16 11:56:58 by Ybkuo            #
# ************************************************ #

import requests
import re
import os

headers = {
    'User-Agent': 'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; \
    .NET CLR 2.0.50727)'
    }


# 判断验证是否存在
def is_code():
    url = 'https://www.douban.com/'
    r = requests.get(url, headers=headers)
    html = r.content.decode('utf-8')
    code_pat = 'src="(https://www.douban.com/misc/captcha\?id=.*?)"'
    result = re.compile(code_pat, re.S).findall(html)
    if result:
        data = {
            'captcha-id': '',
            'captcha-solution': '',
            'form_email': '15313779681',
            'form_password': 'password123',
            'source': 'index_nav'
        }
    else:
        data = {
            'source': 'index_nav',
            'form_email': '15313779681',
            'form_password': 'password123'
        }
    return data,result


# 获取验证码
def code():
    url = 'https://www.douban.com/'
    s = requests.session()
    r = s.get(url, headers=headers)
    html = r.content.decode('utf-8')
    code_pat = 'src="(https://www.douban.com/misc/captcha\?id=.*?)"'
    result = re.compile(code_pat, re.S).findall(html)
    print(result)
    if result:
        data = {
            'captcha-id': '',
            'captcha-solution': '',
            'form_email': '15313779681',
            'form_password': 'password123',
            'source': 'index_nav'
        }
        img = s.get(result[0]).content
        path = '../Pictures/code/1.jpg'
        try:
            with open(path, 'wb') as f:
                f.write(img)
        except FileNotFoundError:
            os.system('mkdir -p ../Pictures/code/')
            with open(path, 'wb') as f:
                f.write(img)
        id_pat = 'id=(.*)&amp;size=s'
        captcha_id = re.compile(id_pat).findall(result[0])
        captcha_solution = input("输入验证码：")
        print(result[0])
        print(captcha_id[0])
        data['captcha-id'] = captcha_id[0]
        data['captcha-solution'] = captcha_solution
    else:
        data = {
            'source': 'index_nav',
            'form_email': '15313779681',
            'form_password': 'password123'
        }
    return data

'''
# get login cookie
def login_info():
    data = code()
    login_url = 'https://www.douban.com/accounts/login'
    # mysqlf_url = 'https://www.douban.com/people/Tousensei/'
    s = requests.session()
    r_p = s.post(login_url, headers=headers, data=data)
    cookies = r_p.cookies
    # r = s.get(mysqlf_url, cookies=r_p.cookies, headers=headers)
    # html = r.content.decode('utf-8')
    # print(html)
'''

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
    return result


# get user address
def info_add(url):
    data = code()
    login_url = 'https://www.douban.com/accounts/login'
    s = requests.session()
    r_p = s.post(login_url, headers=headers, data=data)
    cookies = r_p.cookies
    info_list = info(url)
    for self_info in info_list:
        r = s.get(self_info[0], headers=headers, cookies=cookies)
        html = r.content.decode('utf-8')
        add_pad = '常居:&nbsp;<a.*?>(.*?)</a>'
        result = re.compile(add_pad, re.S).findall(html)
        print(result)


'''
def test():
    # url = "https://www.douban.com/people/77076475/"
    data = code()
    login_url = 'https://www.douban.com/accounts/login'
    # mysqlf_url = 'https://www.douban.com/people/Tousensei/'
    s = requests.session()
    r_p = s.post(login_url, headers=headers, data=data)
    cookies = r_p.cookies

    url="https://www.douban.com/people/Tousensei/"
    r = s.get(url, headers=headers, cookies=cookies)
    html = r.content.decode('utf-8')
    add_pad = '常居:&nbsp;<a.*?>(.*?)</a>'
    result = re.compile(add_pad, re.S).findall(html)
    print(html)
    print(result)
'''


def main():
    url = url = 'https://movie.douban.com/subject/24852545/comments?\
start=00&limit=20&sort=new_score&status=P'
    # print(login_info())
    print(info(url))
    # code()
    # print(is_code())
    # info_add(url)
    # test()
    # login_info()


if __name__ == '__main__':
    main()
