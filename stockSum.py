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
score = 70.00
totalStock = 0
data = {}
data['Fadate'] = time.strftime("%Y-%m-%d", time.localtime())

for page in range(1,100) :
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
			totalStock = totalStock + 1
			print data['Fastockno'],
			print data['Fastockname']

	except urllib2.URLError as e:
		print e.reason
		print e.reason[0]
		print e.reason[1]
	except socket.timeout as e:
		print type(e)    #catched
print str(data['Fadate']) + " Total is " + str(totalStock)

# 打开数据库连接
conn = MySQLdb.connect("localhost","stock","This is not mima","stockdb" )
cursor = conn.cursor()

sql = "INSERT INTO stockdb.dailyCheck VALUES (%s,%s,%s,%s)"
param = (data['Fadate'],
		str(totalStock),
		"0",
		"0")
print sql
cursor = conn.cursor()
try:
	n = cursor.execute(sql,param)
	conn.commit()
	cursor.close()
	print 'insert',n
except:
	print "Error: INSERT SQL wrong"
# 关闭数据库连接
conn.close()
