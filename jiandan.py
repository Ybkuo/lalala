#!/usr/bin/env python
# coding=utf-8
import re
import requests
import base64
import os
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20\
    100101 Firefox/61.0'
}


def ios():
    system = sys.platform
    if system == 'win32':
        OS = 'win'
    else:
        OS = 'linux'
    return OS


def picture(url, page):
    IOS = ios()
    s = requests.session()
    response = s.get(url, headers=headers)
    html = str(response.text)
    pat2 = '<span class="img-hash">(.*)</span>'
    imagelist = re.compile(pat2).findall(html)
    print("第"+str(page)+"页,有"+str(len(imagelist))+"张")
    x = 1
    for img_hash in imagelist:
        imageurl = "http:"+base64.b64decode(img_hash).decode()
        img = requests.get(imageurl).content
        img_path = "../image/"+str(page)+"-"+str(x)+".jpg"
        try:
            file_1 = open(img_path, "wb")
            file_1.write(img)
            file_1.close()
        except Exception as e:
            print('create dir')
            if IOS == 'win':
                os.system('powershell.exe -command "mkdir ../image"')
            else:
                os.system('mkdir ../image')
        x += 1


for i in range(1, 10):
    url = "http://jandan.net/ooxx/page-"+str(i)+"#comments"
    picture(url, i)
