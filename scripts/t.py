#!/usr/bin/python
#coding: utf-8

import MySQLdb

# mysql
host = '192.168.220.201'
db = 'dzhops'
user = 'dzhops'
pw = 'dzhinternet'
port = 3306
serv_sql = '''SELECT * from `servstatus` order by id DESC limit 1'''
try:
    conn = MySQLdb.connect(
        host = host,
        user = user,
        passwd = pw,
        db = db,
        port = port,
        charset='utf8')
    cursor = conn.cursor()
    n = cursor.execute(serv_sql)
    conn.commit()

    for row in cursor.fetchall():
        ret = dict()
        ret['nowtime'] = row[1]
        ret['sysone'] = row[2]
        ret['sysfive'] = row[3]
        ret['sysfifteen'] = row[4]
        ret['cpuperc'] = row[5]
        ret['memtotal'] = row[6]
        ret['memused'] = row[7]
        ret['memperc'] = row[8]
        ret['disktotal'] = row[9]
        ret['diskused'] = row[10]
        ret['diskperc'] = row[11]
except MySQLdb.Error,e:
    unret['MysqlErro'] = e
    ret.undate(unret)

for i in ret.keys():
    print '%s : %s' %(i, ret[i])
