#coding=utf-8
import urllib
import urllib2
import socket
import re
import cookielib
import time  # 引入time模块


data = {}
data['Fastockno'] = '000001'
data['Facostdesc'] = ''

savcook_URL = 'http://stockdata.stock.hexun.com/'+data['Fastockno']+'.shtml'  # 登录用的URL
get_url = 'http://stockdata.stock.hexun.com/zlkp/ggstock.aspx?code='+data['Fastockno']  # 利用cookie请求访问另一个网址


postdata = ''
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
cookie_filename = 'hx_cookie.txt'
cookie_jar = cookielib.MozillaCookieJar(cookie_filename)
handler = urllib2.HTTPCookieProcessor(cookie_jar)
opener = urllib2.build_opener(handler)
  
request = urllib2.Request(savcook_URL, postdata, headers)
try:  
	response = opener.open(request)
except urllib2.URLError as e:
	print(e.code, ':', e.reason)
  
cookie_jar.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中

#for item in cookie_jar:
#	print('Name = ' + item.name)
#	print('Value = ' + item.value)

get_request = urllib2.Request(get_url, headers=headers)

try:
	page = opener.open(get_request)
	html = page.read().decode("gbk").encode("utf-8")
	pattern = re.compile('gkpg.aspx\">(.*?)</a>' +
							'.*?text_01\">(.*?)</p>',re.S)
	items4 = re.findall(pattern,html)
	for item in items4 :
		data['Facostdesc'] = item[1]
		data['Facostdesc'] = data['Facostdesc'].replace('<span style="color: #990000">', '')
		data['Facostdesc'] = data['Facostdesc'].replace('</span>', '')

	print data['Facostdesc']

except urllib2.URLError as e:
	print e
