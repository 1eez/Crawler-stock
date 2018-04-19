#coding=utf-8
import urllib
import urllib2
import socket
import re
import cookielib
import time  # 引入time模块
import MySQLdb  # 引入MySQL模块


#定义五项取分值的临界值，小于该分数的将被忽略掉
score = 70.00
#定义一个字典，用来存储一行记录值
data = {}
data['Faid'] = ''
data['Fadate'] = time.strftime("%Y-%m-%d", time.localtime())
data['Fastockno'] = '000001'
data['Fastockname'] = ''
data['Facloseprice'] = ''
data['Fapermark'] = ''
data['Fapcrmark'] = ''
data['Fapnrmark'] = ''
data['Fapsrmark'] = ''
data['Fapegmark'] = ''
data['Faavgmark'] = ''
data['Faequity'] = ''
data['Fasection'] = ''
data['Falagmoney'] = ''
data['Famidmoney'] = ''
data['Fasmlmoney'] = ''
data['Facostdesc'] = ''
data['Factrldesc'] = ''
SQLNo = 1

###################################
#
#获得数据表中，最大一行的行号
conn = MySQLdb.connect("localhost","stock","This is not mima","stockdb" )
cursor = conn.cursor()

sql = "SELECT MAX(Faid) AS Faid FROM auditionList"
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	for row in results:
		if row[0] == None:
			SQLNo = 1
		else:
			SQLNo = row[0] + 1
except:
	print "Error: get Max Faid by SQL wrong"

###################################
#
#获得和讯网的cookie供costdesc爬虫使用
savcook_URL = 'http://stockdata.stock.hexun.com/'+data['Fastockno']+'.shtml'  # 登录用的URL
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

###################################
#
#定义代理服务器地址，公司内爬虫使用
#proxy_info = { 'host' : 'web-proxy.oa.com','port' : 8080 }
#proxy_support = urllib2.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)


for page in range(1,99) :
	url = "http://datainfo.stock.hexun.com/ssgs/zzcw/jzpg.aspx?page=" + str(page)
	request = urllib2.Request(url)

	try:
		page = urllib2.urlopen(url)
		html = page.read().decode("gbk").encode("utf-8")
		pattern = re.compile('ggjz.aspx\?StockCode=(.*?)\'>'+
						'(.*?)</a>' +
						'.*?align=\'right\'>(.*?)</td>'+
						'.*?align=\'right\'>(.*?)</td>'+
						'.*?align=\'right\'>(.*?)</td>'+
						'.*?align=\'right\'>(.*?)</td>'+
						'.*?align=\'right\'>(.*?)</td>'+
						'.*?align=\'right\'>(.*?)</td>',re.S)
		items1 = re.findall(pattern,html)
		for item in items1 :
			if float(item[3]) < score or float(item[4]) < score or float(item[5]) < score or float(item[6]) < score or float(item[7]) < score :
				continue
			data['Fastockno'] = item[0]
			data['Fastockname'] = item[1].replace(' ', '')
			data['Facloseprice'] = item[2]
			data['Fapermark'] = item[3]
			data['Fapcrmark'] = item[4]
			data['Fapnrmark'] = item[5]
			data['Fapsrmark'] = item[6]
			data['Fapegmark'] = item[7]
			data['Faavgmark'] = float(sum([float(item[3]), float(item[4]), float(item[5]), float(item[6]), float(item[7])]) / 5)

			print data['Fadate'],
			print data['Fastockno'],
			print data['Fastockname'],
			print data['Fapermark'],
			print data['Fapcrmark'],
			print data['Fapnrmark'],
			print data['Fapsrmark'],
			print data['Fapegmark'],
			print data['Faavgmark']

			if data['Fastockno'][0:1] == '0' :
				urltype = '1'
			elif data['Fastockno'][0:1] == '6' :
				urltype = '0'

			url = "http://quotes.money.163.com/"+urltype+data['Fastockno']+".html"
			request = urllib2.Request(url)

			try:
				page = urllib2.urlopen(url)
				html = page.read()

				pattern = re.compile('price:\s\'(.*?)\','+
									'.*?主营业务：\s(.*?)</p>'+
									'.*?流通股本：\s(.*?)</p>'+
									'.*?zjlxChart1.*?value":"(.*?)"}'+
									'.*?value":"(.*?)"}'+
									'.*?value":"(.*?)"}',re.S)
				items2 = re.findall(pattern,html)
				for item in items2 :
					data['Facloseprice'] = item[0]
					data['Faequity'] = item[2].replace('\n', '')
					data['Faequity'] = data['Faequity'].replace(' ', '')
					data['Faequity'] = data['Faequity'].replace(',', '')
					data['Faequity'] = data['Faequity'].replace('万股', '')
					data['Faequity'] = str(float(int(data['Faequity']) * float(data['Facloseprice']) / 10000))
					data['Fasection'] = item[1].replace('\n', '')
					data['Fasection'] = data['Fasection'].replace(' ', '')
					data['Fasection'] = data['Fasection'].replace('<td>', '')
					data['Fasection'] = data['Fasection'].replace('</td>', '')
					data['Falagmoney'] = item[3]
					data['Famidmoney'] = item[4]
					data['Fasmlmoney'] = item[5]
				print data['Facloseprice'],
				print data['Faequity'],
				print data['Fasection'],
				print data['Falagmoney'],
				print data['Famidmoney'],
				print data['Fasmlmoney']

			except urllib2.URLError as e:
				print e.reason
				print e.reason[0]
				print e.reason[1]
			except socket.timeout as e:
				print type(e)    #catched

			url = "http://stockpage.10jqka.com.cn/"+data['Fastockno']+"/"
			request = urllib2.Request(url)

			try:
				page = urllib2.urlopen(url)
				html = page.read()

				pattern = re.compile('\"zjlxlstj_txt\">(.*?)</p>'+
									'.*?title=\"(.*?)\">',re.S)
				items3 = re.findall(pattern,html)
				for item in items3 :
					data['Factrldesc'] = item[0].replace('<i class="cred">', '')
					data['Factrldesc'] = data['Factrldesc'].replace('<i class="cgreen">', '')
					data['Factrldesc'] = data['Factrldesc'].replace('</i>', '')
					data['Factrldesc'] = data['Factrldesc'] + item[1].replace(' ', '')

				print data['Factrldesc']

			except urllib2.URLError as e:
				print e
			except socket.timeout as e:
				print type(e)    #catched

			get_url = 'http://stockdata.stock.hexun.com/zlkp/ggstock.aspx?code='+data['Fastockno']  # 利用cookie请求访问另一个网址

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

			sql = "INSERT INTO stockdb.auditionList VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			param = (str(SQLNo),
					data['Fadate'],
					data['Fastockno'],
					data['Fastockname'],
					data['Facloseprice'],
					data['Fapermark'],
					data['Fapcrmark'],
					data['Fapnrmark'],
					data['Fapsrmark'],
					data['Fapegmark'],
					str(round(data['Faavgmark'],2)),
					str(round(float(data['Faequity']),2)),
					data['Fasection'],
					data['Falagmoney'],
					data['Famidmoney'],
					data['Fasmlmoney'],
					data['Facostdesc'],
					data['Factrldesc'])
			print sql
			cursor = conn.cursor()
			try:
				n = cursor.execute(sql,param)
				conn.commit()
				cursor.close()
				SQLNo = SQLNo + 1
				print 'insert',n
			except:
				print "Error: INSERT SQL wrong"

	except urllib2.URLError as e:
		print e
	except socket.timeout as e:
		print type(e)    #catched

# 关闭数据库连接
conn.close()


