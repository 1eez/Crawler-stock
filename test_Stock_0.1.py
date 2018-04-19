#coding=utf-8
import urllib
import urllib2
import socket
import re
import time  # 引入time模块
import MySQLdb

# The proxy address and port:
#proxy_info = { 'host' : 'web-proxy.oa.com','port' : 8080 }
# We create a handler for the proxy
#proxy_support = urllib2.ProxyHandler({"http" : "http://%(host)s:%(port)d" % proxy_info})
# We create an opener which uses this handler:
#opener = urllib2.build_opener(proxy_support)
# Then we install this opener as the default opener for urllib2:
#urllib2.install_opener(opener)

#定义五项取分值的临界值，小于该分数的将被忽略掉
score = 80.00
#定义一个字典，用来存储一行记录值
data = {}
data['Faid'] = ''
data['Fadate'] = time.strftime("%Y-%m-%d", time.localtime())
data['Fastockno'] = ''
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

# 打开数据库连接
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
	print "Error: SELECT SQL wrong"


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
		items = re.findall(pattern,html)
		for item in items :
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
			print data['Facloseprice'],
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

				pattern = re.compile('主营业务：\s(.*?)</p>'+
									'.*?总&nbsp;股&nbsp;本：\s(.*?)</p>'+
									'.*?流通股本：\s(.*?)</p>'+
									'.*?zjlxChart1.*?value":"(.*?)"}'+
									'.*?value":"(.*?)"}'+
									'.*?value":"(.*?)"}',re.S)
				items = re.findall(pattern,html)
				for item in items :
					data['Faequity'] = item[1].replace('\n', '')
					data['Faequity'] = data['Faequity'].replace(' ', '')
					data['Faequityfa'] = item[2].replace('\n', '')
					data['Faequityfa'] = data['Faequityfa'].replace(' ', '')
					data['Fasection'] = item[0].replace('\n', '')
					data['Fasection'] = data['Fasection'].replace(' ', '')
					data['Fasection'] = data['Fasection'].replace('<td>', '')
					data['Fasection'] = data['Fasection'].replace('</td>', '')
					data['Falagmoney'] = item[3]
					data['Famidmoney'] = item[4]
					data['Fasmlmoney'] = item[5]
				print data['Faequity'],
				print data['Faequityfa'],
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
				items = re.findall(pattern,html)
				for item in items :
					data['Factrldesc'] = item[0].replace('<i class="cred">', '')
					data['Factrldesc'] = data['Factrldesc'].replace('<i class="cgreen">', '')
					data['Factrldesc'] = data['Factrldesc'].replace('</i>', '')
					data['Factrldesc'] = data['Factrldesc'] + item[1].replace(' ', '')

				print data['Factrldesc']

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
						data['Faequity'],
						str(round(data['Faequityfa'],2)),
						data['Fasection'],
						data['Falagmoney'],
						data['Famidmoney'],
						data['Fasmlmoney'],
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
				print e.reason
				print e.reason[0]
				print e.reason[1]
			except socket.timeout as e:
				print type(e)    #catched

	except urllib2.URLError as e:
		print e.reason
		print e.reason[0]
		print e.reason[1]
	except socket.timeout as e:
		print type(e)    #catched

# 关闭数据库连接
conn.close()

