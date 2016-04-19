# coding=utf-8

import urllib2, urllib, json


class SaltAPI(object):
    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
        self.__token_id = self.saltLogin()

    def saltLogin(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token': ''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    def asyncMasterToMinion(self, tgt, fun, arg):
        '''
        异步执行，当target为部分minion时，Master操作Minion；
        :param target: 目标服务器ID组成的字符串；
        :param fun: 使用的salt模块，如state.sls, cmd.run
        :param arg: 传入的命令或sls文件
        :return: jid字符串
        '''
        if tgt == '*':
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid


    def masterToMinionContent(self, tgt, fun, arg):
        '''
            Master控制Minion，返回的结果是内容，不是jid；
            目标参数tgt是一个如下格式的字符串：'*' 或 'zhaogb-201, zhaogb-202, zhaogb-203, ...'
        '''
        if tgt == '*':
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        result = content['return'][0]
        return result