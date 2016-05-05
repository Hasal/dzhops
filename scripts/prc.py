#!/usr/bin/python
# coding: utf-8

import subprocess
import MySQLdb

def ExecCmd(cmd):
    child = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    retno = child.wait()
    return retno

# mysql
host = '数据库地址'
db = '库名'
user = '用户'
pw = '密码'
port = 端口

saltcmd = 'ps -ef|grep salt-master|grep -v grep'
apicmd = 'ps -ef|grep salt-api|grep -v grep'
mycmd = 'ps -ef|grep mysql|grep -v grep'
snmpcmd = 'ps -ef|grep snmpd|grep -v grep'

saltproc = ExecCmd(saltcmd)
apiproc = ExecCmd(apicmd)
myproc = ExecCmd(mycmd)
snmproc = ExecCmd(snmpcmd)

#print saltproc,apiproc,myproc,snmproc

#save to mysql
proc_sql = '''INSERT INTO `index_procstatus`
        (`nowtime`,`saltproc`,`apiproc`,`myproc`,`snmproc`)
        VALUES
        (now(), %s, %s, %s, %s)'''
conn = MySQLdb.connect(
        host = host,
        user = user,
        passwd = pw,
        db = db,
        port = port,
        charset='utf8')
cursor = conn.cursor()
try:
    cursor.execute(proc_sql, (saltproc, apiproc, myproc, snmproc))
    conn.commit()

except MySQLdb.Error,e:
    # Rollback in case there is any error
    #mysqlErro = "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.rollback()
