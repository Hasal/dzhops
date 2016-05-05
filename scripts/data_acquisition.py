#!/usr/bin/python
# -*- coding: utf-8 -*-
# Guibin created on 2015/10/21
# version: 0.01

from __future__ import division
import MySQLdb
import subprocess
import math
from decimal import Decimal

# mysql
host = '数据库地址'
db = '库名'
user = '用户'
pw = '密码'
port = 端口

# snmp command
sysone = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.1 |cut -d ':' -f 4|tr -d '[:blank:]'"
sysfive = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.2 |cut -d ':' -f 4|tr -d '[:blank:]'"
sysfifteen = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.10.1.3.3 |cut -d ':' -f 4|tr -d '[:blank:]'"

cpuidle = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.11.11.0 |cut -d ':' -f 4|tr -d '[:blank:]'"

memtotal = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.4.5.0 |cut -d ':' -f 4|tr -d '[:blank:]'"
memfree = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.4.6.0 |cut -d ':' -f 4|tr -d '[:blank:]'"

disktotal = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.9.1.6.1 |cut -d ':' -f 4|tr -d '[:blank:]'"
diskused = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.9.1.8.1 |cut -d ':' -f 4|tr -d '[:blank:]'"
diskperc = "snmpget -v 2c -c public localhost .1.3.6.1.4.1.2021.9.1.9.1  |cut -d ':' -f 4|tr -d '[:blank:]'"

# exec function
def ExecSnmp(getsnmp):
    child = subprocess.Popen(getsnmp, shell=True, stdout=subprocess.PIPE)
    child.wait()
    middle_res = child.stdout.read()
    result = middle_res.strip('\n')
    return result

def SaveMy(sql):
    conn = MySQLdb.connect(
            host = host,
            user = user,
            passwd = pw,
            db = db,
            port = port,
            charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()

    except MySQLdb.Error,e:
        # Rollback in case there is any error
        #mysqlErro = "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()

#get monitor data
sysload1 = ExecSnmp(sysone)
sysload5 = ExecSnmp(sysfive)
sysload15 = ExecSnmp(sysfifteen)

cpuidl = ExecSnmp(cpuidle)
cpuused = str(100 - int(cpuidl))

memtol = ExecSnmp(memtotal)
memfre = ExecSnmp(memfree)
memperc = str(100 - int(round(int(memfre[:-2])/int(memtol[:-2])*100)))
memtolg = str(int(math.ceil(int(memtol[:-2])/1024/1024)))
memusdg = Decimal(str(round((int(memtol[:-2]) - int(memfre[:-2]))/1024/1024,2)))

disktol = ExecSnmp(disktotal)
diskusd = ExecSnmp(diskused)
diskpr = ExecSnmp(diskperc)

dktotal =  str(int(math.ceil(int(disktol)/1024/1024)))
dkused = Decimal(str(round(int(diskusd)/1024/1024,1)))

#save to mysql
serv_sql = '''INSERT INTO `index_servstatus`
        (`nowtime`,`sysone`,`sysfive`,`sysfifteen`,`cpuperc`,`memtotal`,`memused`,`memperc`,`disktotal`,`diskused`,`diskperc`)
        VALUES
        (now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
conn = MySQLdb.connect(
        host = host,
        user = user,
        passwd = pw,
        db = db,
        port = port,
        charset='utf8')
cursor = conn.cursor()
try:
    cursor.execute(serv_sql, (sysload1,sysload5,sysload15,cpuused,memtolg,memusdg,memperc,dktotal,dkused,diskpr))
    conn.commit()

except MySQLdb.Error,e:
    # Rollback in case there is any error
    #mysqlErro = "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.rollback()

#print 'system load : %s, %s, %s' % (sysload1, sysload5, sysload15)
#print 'CPU used perc: %d%%' % cpuused
#print 'Mem used perc: %d%%' % memperc
#print 'Mem : %s/%d' % (memusdg, memtolg)
#print 'Disk : %s/%d  %s%%' % (dktotal, dkused, diskpr)

