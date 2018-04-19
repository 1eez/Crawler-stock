#coding=utf-8

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost","stock","This is not mima","stockdb" )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM userList \
      WHERE Fuopenid <>''"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      Fuopenid = row[0]
      Funick = row[1]
      Funame = row[2]
      Fupermission = row[3]
      Fucreatedate = row[4]
      # 打印结果
      print "Fuopenid=%s,Funick=%s,Funame=%s,Fupermission=%s,Fucreatedate=%s" % \
             (Fuopenid, Funick, Funame, Fupermission, Fucreatedate )
except:
   print "Error: unable to fecth data"

# 关闭数据库连接
db.close()