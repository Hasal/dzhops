#!/usr/bin/python
# -*- coding: utf-8 -*-
# Guibin created on 2015/10/26
# version: 0.01

import sys,MySQLdb,urllib
sys.path.append('/opt/dzhops')
from dzhops import settings
from common.saltapi import SaltAPI

class scriptApi(SaltAPI):
    def mini_status(self):
        '''
        {u'return': [{u'down': [u'zhaogb-202'], u'up': [u'zhaogb-203', u'zhaogb-212', u'zhaogb-220']}]}
        '''
        params = {"client":"runner","fun":"manage.status"}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        mini_up = content['return'][0]['up']
        mini_down = content['return'][0]['down']
        return mini_up,mini_down
ret = {}
try:
    sapi = scriptApi(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    minions,minions_pre,minions_rej = sapi.list_all_key()
    mini_up, mini_down = sapi.mini_status()

    ret['num_mini'] = len(minions)
    ret['num_minipre'] = len(minions_pre)
    ret['num_minirej'] = len(minions_rej)

    ret['num_miniup'] = len(mini_up)
    ret['num_minidown'] = len(mini_down)
    ret['num_miniall'] = ret['num_miniup'] + ret['num_minidown']

except Exception,e:
    print str(e)
    ret['num_mini'] = '0'
    ret['num_minipre'] = '0'
    ret['num_minirej'] = '0'

    ret['num_miniup'] = '0'
    ret['num_minidown'] = '0'
    ret['num_miniall'] = '0'

conf = settings.DATABASES['default']
mikey_sql = '''INSERT INTO `index_minikeys`
        (`nowtime`,`miniall`,`minion`,`miniout`,`keyall`,`keypre`,`keyrej`)
        VALUES
        (now(), %s, %s, %s, %s, %s, %s)'''

conn = MySQLdb.connect(
        host = conf['HOST'],
        user = conf['USER'],
        passwd = conf['PASSWORD'],
        db = conf['NAME'],
        port = conf['PORT'],
        charset='utf8')
cursor = conn.cursor()
try:
    cursor.execute(mikey_sql, (ret['num_miniall'],ret['num_miniup'],ret['num_minidown'],ret['num_mini'],ret['num_minipre'],ret['num_minirej']))
    conn.commit()

except MySQLdb.Error,e:
    # Rollback in case there is any error
    #mysqlErro = "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.rollback()
