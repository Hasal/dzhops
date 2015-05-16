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


def salt_key_list(request):
    """
    list all key 
    """

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

def tgtCheck():
    """
    legitimate target test
    in  : ['zhaogb-201','zhaogb-202','dzh-wgq101','dzh-wgq223','dzh-wgq233']
    out : ['zhaogb-201','zhaogb-202','dzh-wgq101','dzh-wgq223','dzh-wgq233','zhaogb-*','dzh-wgq*','*'],['zhaogb-201','zhaogb-202','dzh-wgq115',...],['zhaogb-','dzh-wgq',...]
    """
    
    groupli = []
    grouplinox = []
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])  
    minions,minions_pre = sapi.list_all_key()
    miniaccept = minions[:]
    
    for mini in miniaccept:
        hostskey = re.sub(r'[0-9]', '', mini)
        groupkey = hostskey + '*'
        grouplinox.append(hostskey)
        groupli.append(groupkey)
    grouptgt = list(set(groupli))
    grouptgt.append('*')
    grouptgt.extend(minions)
    tgtTuple = tuple(grouptgt)
    return tgtTuple,minions,grouplinox
    
    
def module_deploy(request):
    """
    deploy (mobile/manager/info..) module
    out  ret:{'host1':{'cont':'format result','status': colour },...} , hostsft:{'sum':'','rsum':'','unre':'','unrestr':'','fa':'','tr':''}
    """

    ret = {}
    unret = {}
    valcon = {}
    hostsft = {}
    jid = []
    #liv = []
    objlist = []
    hostfa = 0
    hosttr = 0
    hostsum = 0
    hostrsum = 0
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtTest,tgtminis,tgtminisnox = tgtCheck()
            tgtlist = tgt.split(',')
            if tgt:
                if tgt in tgtTest:
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
                                result = db.select_table(settings.RETURNS_MYSQL,sql,str(i))
                                
                                #result = {'zhaogb-201':{'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed': {'comment': 'zhaogb-201', 'name': '/usr/lib64/libodbc.so.1', 'start_time': 'zhaogb-201', 'result': True, 'duration': 'zhaogb-201', '__run_num__': 2, 'changes': {}}},'zhaogb-202':{'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed': {'comment': 'zhaogb-202', 'name': 'zhaogb-202', 'start_time': 'zhaogb-202', 'result': True, 'duration': 'zhaogb-202', '__run_num__': 2, 'changes': {'diff': 'New file', 'mode': '0644'}}}}
                                
                                hostrsum = len(result)
                                returnset = set(result.keys())

                            for ka,va in result.iteritems():
                                # result {'zhaogb-201':{},'zhaobg-202':{}}
                                # ka zhaogb-201,zhaogb-202
                                # va {'mo_watch':{'comment':'','result':'',...}}
                                valcon = {}
                                longstrva = ''
                                falseStatus = 0
                                trueStatus = 0
                                liv = []
                                for kva in va.keys():
                                    # kva mo_watch,...
                                    liva = kva.split('_|-')
                                    liv.append(va[kva]['result'])
                                    strva = '结果 : {0}\n标签 : {1}\n操作 : {2}\n开始 : {3}\n耗时 : {4} ms\n变动 : {5}\n{6}\n'.format(va[kva]['result'],liva[1],va[kva]['comment'],va[kva]['start_time'],va[kva]['duration'],va[kva]['changes'],'------------------------------------------------------------')
                                    longstrva += strva

                                if False in liv:
                                    colour = 'False'
                                    hostfa += 1
                                elif True in liv:
                                    colour = 'True'
                                    hosttr += 1
                                else:
                                    pass
                                    # error write to logging
                                    
                                totalStatus = len(liv)
                                for livStatus in liv:
                                    if livStatus == False:
                                        falseStatus += 1
                                    elif livStatus == True:
                                        trueStatus += 1
                                    else:
                                        pass
                                        # error write to logging                                    
                                
                                longstrva += '失败 : {0}\n成功 : {1}\n总计 : {2}'.format(falseStatus, trueStatus, totalStatus)

                                valcon['status'] = colour
                                valcon['cont'] = longstrva
                                unret[ka] = valcon
                            if tgt == '*':
                                hostsum = len(tgtminis)
                                sumset = set(tgtminis)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))
                            elif '*' in tgt:
                                tgtnox = re.sub(r'\*','',tgt)
                                for linox in tgtminisnox:
                                    if tgtnox == linox:
                                        hostsum += 1
                                tgtmat = tgtnox + '[0-9]+'
                                for mini in tgtminis:
                                    matchObj = re.search(tgtmat,mini, re.M|re.I)
                                    if matchObj:
                                        objlist.append(matchObj.group())
                                sumset = set(objlist)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))

                            else:
                                hostsum = len(tgtlist)
                                sumset = set(tgtlist)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))
                            
                            hostsft['sum'] = hostsum
                            hostsft['rsum'] = hostrsum
                            hostsft['unre'] = hostunre
                            hostsft['unrestr'] = hostunrestr
                            hostsft['fa'] = hostfa
                            hostsft['tr'] = hosttr

                        else:
                            valcon['status'] = 'False'
                            valcon['cont'] = '虽然我很菜，但这个不是我的问题，Salt Stack不支持同时执行多个模板。不过我正在尝试通过异步处理来支持！'
                            unret['亲，Salt Stack不支持同时执行多个模板'] = valcon
                    else:
                        valcon['status'] = 'False'
                        valcon['cont'] = '亲，为何不选择一个模块试试呢！'
                        unret['请选择将要部署的模块'] = valcon
                else:
                    valcon['status'] = 'False'
                    valcon['cont'] = '目标主机只能形如zhaogb-201、zhaogb-*、* 这三种！'
                    unret['目标主机不合法'] = valcon
            else:
                valcon['status'] = 'False'
                valcon['cont'] = '需要指定目标主机，才能执行相应模板！'
                unret['亲，木有指定目标主机'] = valcon
    if unret:
        ret = unret
        #ret = {'zhaogb-201':{'cont':'zhaogb-201','status': 'True'},'zhaogb-202':{'cont':'zhaogb-202','status': 'Fasle'},'zhaogb-203':{'cont':'zhaogb-203','status': 'Fasle'},'zhaogb-205':{'cont':'zhaogb-205','status': 'True'}}
    else:
        valcon['status'] = 'False'
        valcon['cont'] = '骚年，你不相信我，就算点开看，也还是没有返回结果！'
        ret['没有返回任何结果'] = valcon
            
    return render_to_response('salt_module_deploy.html', 
           {'ret': ret, 'hostsft': hostsft},context_instance=RequestContext(request)) 

def module_update(request):
    """
    update (mobile/class/prog..etc) module
    out  {'host1':{'cont':'format result','status': colour },...}
    """

    ret = {}
    unret = {}
    valcon = {}
    hostsft = {}
    jid = []
    liv = []
    objlist = []
    hostfa = 0
    hosttr = 0
    hostsum = 0
    hostrsum = 0
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'update':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtTest,tgtminis,tgtminisnox = tgtCheck()
            tgtlist = tgt.split(',')
            if tgt:
                if tgt in tgtTest:
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
                                result = db.select_table(settings.RETURNS_MYSQL,sql,str(i))
                                hostrsum = len(result)
                                returnset = set(result.keys())

                            for ka,va in result.iteritems():
                                for kva in va.keys():
                                    liv.append(va[kva]['result'])
                                if False in liv:
                                    colour = 'False'
                                    hostfa += 1
                                else:
                                    colour = 'True'
                                    hosttr += 1
                                valcon['status'] = colour
                                valcon['cont'] = va
                                unret[ka] = valcon
                            if tgt == '*':
                                hostsum = len(tgtminis)
                                sumset = set(tgtminis)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))
                            elif '*' in tgt:
                                tgtnox = re.sub(r'\*','',tgt)
                                for linox in tgtminisnox:
                                    if tgtnox == linox:
                                        hostsum += 1
                                tgtmat = tgtnox + '[0-9]+'
                                for mini in tgtminis:
                                    matchObj = re.search(tgtmat,mini, re.M|re.I)
                                    if matchObj:
                                        objlist.append(matchObj.group())
                                sumset = set(objlist)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))

                            else:
                                hostsum = len(tgtlist)
                                sumset = set(tgtlist)
                                diffset = sumset - returnset
                                hostunre = len(diffset)
                                hostunrestr = ','.join(list(diffset))
                            
                            hostsft['sum'] = hostsum
                            hostsft['rsum'] = hostrsum
                            hostsft['unre'] = hostunre
                            hostsft['unrestr'] = hostunrestr
                            hostsft['fa'] = hostfa
                            hostsft['tr'] = hosttr

                        else:
                            valcon['status'] = 'False'
                            valcon['cont'] = '虽然我很菜，但这个不是我的问题，Salt Stack不支持同时执行多个模板。不过我正在尝试通过异步处理来支持！'
                            unret['亲，Salt Stack不支持同时执行多个模板'] = valcon
                    else:
                        valcon['status'] = 'False'
                        valcon['cont'] = '亲，为何不选择一个模块试试呢！'
                        unret['请选择将要部署的模块'] = valcon
                else:
                    valcon['status'] = 'False'
                    valcon['cont'] = '目标主机只能形如zhaogb-201、zhaogb-*、* 这三种！'
                    unret['目标主机不合法'] = valcon
            else:
                valcon['status'] = 'False'
                valcon['cont'] = '需要指定目标主机，才能执行相应模板！'
                unret['亲，木有指定目标主机'] = valcon
    if unret:
        ret = unret
    else:
        valcon['status'] = 'False'
        valcon['cont'] = '骚年，你不相信我，就算点开看，也还是没有返回结果！'
        ret['没有返回任何结果'] = valcon

    return render_to_response('salt_module_update.html', 
           {'ret': ret, 'hostsft': hostsft},context_instance=RequestContext(request)) 

def remote_execution(request):
    """
    remote command execution
    out(type:string)    ret = 'format string' 
    """

    ret = ''
    tret = ''
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'exec':
            tgt = request.POST.get('tgt')
            arg = request.POST.get('arg')
            tgtTest,tgtminis,tgtminisnox = tgtCheck()
            dangerCmd = ('rm','reboot','init','shutdown','poweroff')
        if tgt:
            if tgt in tgtTest:
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
                ret = '目标主机不合法，只能形如zhaogb-201、zhaogb-*、* ！'
        else:
            ret = '没有指定目标主机，请重新输入！'
         
    return render_to_response('salt_remote_execution.html',
           {'ret': ret},context_instance=RequestContext(request)) 

