//升级python至 2.7.3

1、下载安装压缩包
wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz

2、解压
从WDCP进入文件管理，/root，手动解压缩。

3、进入文件夹（注意大小写）
cd Python-2.7.3

4、在编译前先在/usr/local建一个文件夹python27（作为python的安装路径，以免覆盖老的版本）
mkdir /usr/local/python27

5、在解压缩后的目录下编译安装，复制粘贴如下命令行
./configure --prefix=/usr/local/python27
make
make install

6、此时没有覆盖老版本，再将原来/usr/bin/python链接改为别的名字
mv /usr/bin/python /usr/bin/python_old

7、再建立新版本python的链接
ln -s /usr/local/python27/bin/python2.7 /usr/bin/python

8、　这个时候输入python，就会显示出python的新版本信息

//下载安装setup tools
1、浏览器到：https://pypi.python.org/pypi/setuptools
2、下载最新工具：setuptools-38.4.0.zip
3、上传到服务器/root
4、通过WDCP，解压缩
5、进入目录 cd setuptools-38.4.0
6、运行命令：python setup.py install

//安装Python 连接 MySQL驱动
1、浏览器到：https://pypi.python.org/pypi/MySQL-python/
2、下载最新版的驱动（当前1.2.5）
3、上传到服务器/root
4、通过WDCP，解压缩
5、进入目录 cd MySQL-python-1.2.5
6、查找mysql-config的位置：find / -name mysql_config
7、复制找到的结果“/www/wdlinux/mysql-5.5.48/bin/mysql_config”
8、修改解压缩目录下的“site.cfg”文件
9、改成（去掉前面井号）：mysql_config = /www/wdlinux/mysql-5.5.48/bin/mysql_config
10、执行代码
python setup.py build
python setup.py install

11、测试是否安装成功
python 后， import MySQLdb，不报错，就是安装成功了。


//脚本语言修改属性为可执行
chmod +x filename.sh



数据库：stockdb
用户名：stock
密码：this is not mima

运行命令：
python /www/web/admin/public_html/stockSum.py
python /www/web/admin/public_html/Stock.py


//创建库表 —— 海选日表

//字段列表中文描述如下：

//表主键ID
//写入日期
//股票代码
//股票名称
//收盘价
//市盈率得分
//市现率得分
//市净率得分
//市售率得分
//PEG得分
//综合得分
//流通股本
//所属板块
//大单流向
//中单流向
//小单流向
//主力成本描述
//控盘描述

create table auditionList(
    Faid int not null,
    Fadate date null,
    Fastockno varchar(8) null,
    Fastockname varchar(16) null,
    Facloseprice DECIMAL(9,3) null,
    Fapermark DECIMAL(5,2) null,
    Fapcrmark DECIMAL(5,2) null,
    Fapnrmark DECIMAL(5,2) null,
    Fapsrmark DECIMAL(5,2) null,
    Fapegmark DECIMAL(5,2) null,
    Faavgmark DECIMAL(5,2) null,
    Faequity DECIMAL(9,2) null,
    Fasection varchar(64) null,
    Falagmoney DECIMAL(9,2) null,
    Famidmoney DECIMAL(9,2) null,
    Fasmlmoney DECIMAL(9,2) null,
	Facostdesc varchar(256) null,
	Factrldesc varchar(256) null,
    primary key(Faid)
)engine=InnoDB;

//增加索引-海选日表

ALTER TABLE `auditionList` ADD INDEX ( `Fadate` );
ALTER TABLE `auditionList` ADD INDEX ( `Fastockno` );
ALTER TABLE `auditionList` ADD INDEX ( `Fastockname` );

//创建库表 —— 每日对账表

create table dailyCheck(
	Fddate date not null,
	Fdsumcount int null,
	Fddetailcount int null,
    Fdemptycount int null
)engine=InnoDB;

ALTER TABLE `dailyCheck` ADD INDEX ( `Fddate` );


//修改MySQL stock 用户权限，用于使用存储过程

grant create routine on stockdb.* to stock@localhost;
grant alter routine on stockdb.* to stock@localhost;
grant execute on stockdb.* to stock@localhost;

//用命令行的方式创建存储过程

DELIMITER //
CREATE PROCEDURE proc_stock()
BEGIN
   UPDATE dailyCheck Table2 INNER JOIN (SELECT Fadate, count(Faid) AS Fcount FROM auditionList GROUP BY Fadate) Table1 SET Table2.Fddetailcount = Table1.Fcount WHERE Table2.Fddate = Table1.Fadate;
END;
//
DELIMITER ;


//一大堆SQL语句

UPDATE dailyCheck Table2 INNER JOIN (SELECT Fadate, count(Faid) AS Fcount FROM auditionList GROUP BY Fadate) Table1 SET Table2.Fddetailcount = Table1.Fcount WHERE Table2.Fddate = Table1.Fadate;

SELECT Fddate, Fdsumcount, Fcount FROM dailyCheck Table2, (SELECT Fadate, count(Faid) AS Fcount FROM auditionList GROUP BY Fadate) Table1 WHERE Table2.Fddate = Table1.Fadate

SELECT Fadate, count(Faid) AS Fcount FROM auditionList GROUP BY Fadate

INSERT INTO stockdb.auditionList VALUES (1,"2018-1-18","0001","Name",1.0,2.0,3.0,4.0,5.0,6.0,7.0,"Faequity","Faequityfa","Fasection",8.0,9.0,10.0,"Factrldesc");

