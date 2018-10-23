import requests
import re

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20\
100101 Firefox/61.0'
}


def popular(url, page):
	x = 1
	s = requests.session()
	r = s.get(url, headers=headers)
	html = str(r.text)
	userpat = '<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>'
	userlist = re.compile(userpat, re.S).findall(html)
	for show_content in userlist:
		# path = "book/1.txt"
		user = show_content[0].strip('\n')
		content = show_content[1].strip('\n')
		a = "用户"+str(page)+"-"+str(x)+"是："+user+"\n"
		b = "内容是："+content.replace('<br/>', '')+"\n"
		str_txt = a+b+"\n"
		print(str_txt)
		# with open(path, "a", encoding="utf-8") as f:
		# f.write(str_txt)
		x += 1


for i in range(1, 2):
	url = "https://www.qiushibaike.com/text/page/"+str(i)+"/"
	popular(url, i)
