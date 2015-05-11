# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from common.saltapi import SaltAPI
from dzhops import settings
from dzhops.mysql import db_operate
from hostlist.models import HostList
import time
import logging

# Import python libs
from numbers import Number
import re
import json

# Import salt libs
#import salt.utils
#import salt.output
#from salt._compat import string_types
#import salt

def salt_key_list(request):
    """
    list all key 
    """

#    user = request.user
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    minions,minions_pre = sapi.list_all_key() 
    
    return render_to_response('salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre}) 

def salt_accept_key(request):
    """
    accept salt minions key
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    ret = sapi.accept_key(node_name)
    return HttpResponseRedirect(reverse('key_list')) 

def salt_delete_key(request):
    """
    delete salt minions key
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    ret = sapi.delete_key(node_name)
    return HttpResponseRedirect(reverse('key_list'))

def module_deploy(request):
    """
    deploy (nginx/php/mysql..etc) module
    """

    ret = {}
    unret = {}
    jid = []
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            if tgt:
                if arg:
                    if len(arg) < 2:
                        sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
                        for i in arg:
                            obj = sapi.async_deploy(tgt,i)
                            jid.append(obj)
                        db = db_operate()
                        for i in jid:
                            time.sleep(30)
                            sql = 'select id,`return` from salt_returns where jid=%s'
                            unret = db.select_table(settings.RETURNS_MYSQL,sql,str(i))
                    else:
                        unret['亲，Salt Stack不支持同时执行多个模板'] = '虽然我很菜，但这个不是我的问题，Salt Stack不支持同时执行多个模板。不过我正在尝试通过异步处理来支持同时部署多个模块！'
                else:
                    unret['请选择将要部署的模块'] = '亲，为何不选择一个模块试试呢！'
            else:
                unret['亲，没有指定目标主机'] = '友情提示，你木有指定目标主机！'
    if unret:
        ret = unret
    else:
        ret['没有返回任何结果'] = '骚年，你不相信我，就算点开看，也还是没有返回结果！'
            
    return render_to_response('salt_module_deploy.html', 
           {'ret': ret},context_instance=RequestContext(request)) 

def module_update(request):
    """
    update (mobile/class/prog..etc) module
    """

    ret = {}
    unret = {}
    jid = []
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'update':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            if tgt:
                if arg:
                    if len(arg) < 2:
                        sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
                        for i in arg:
                            obj = sapi.async_deploy(tgt,i)
                            jid.append(obj)
                        db = db_operate()
                        for i in jid:
                            time.sleep(30)
                            sql = 'select id,`return` from salt_returns where jid=%s'
                            unret = db.select_table(settings.RETURNS_MYSQL,sql,str(i))
                    else:
                        unret['亲，Salt Stack不支持同时执行多个模板'] = '虽然我很菜，但这个不是我的问题，Salt Stack不支持同时执行多个模板。不过我正在尝试通过异步处理来支持同时部署多个模块！'
                else:
                    unret['请选择将要更新的模块'] = '亲，为何不选择一个模块试试呢！'
            else:
                unret['亲，没有指定目标主机'] = '友情提示，你木有指定目标主机！'
    if unret:
        ret = unret
    else:
        ret['没有返回任何结果'] = '骚年，你不相信我，就算点开看，也还是没有返回结果！'

    return render_to_response('salt_module_update.html', 
           {'ret': ret},context_instance=RequestContext(request)) 

def remote_execution(request):
    """
    remote command execution
    """

    ret = ''
    tret = ''
    dangerCmd = ('rm','reboot','init','shutdown','poweroff')
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'exec':
            tgt = request.POST.get('tgt')
            arg = request.POST.get('arg')    
        if tgt:
            if arg:
                argCmd = arg.split()[0]
                argCheck = argCmd not in dangerCmd
                if argCheck:
                    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                    unret = sapi.remote_execution(tgt,'cmd.run',arg)
                    for kret in unret.keys():
                        lret = kret + ':\n' + unret[kret] + '\n'
                        tret += lret + '\n'
                    ret = tret
                elif not argCheck:
                    ret = '亲，命令很危险, 你这样子老大会不开森！'
            else:
                ret = '没有输入命令，请重新输入！'
        else:
            ret = '没有指定目标主机，请重新输入！'
         
    return render_to_response('salt_remote_execution.html',
           {'ret': ret},context_instance=RequestContext(request)) 

