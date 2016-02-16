# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from common.saltapi import SaltAPI
from dzhops import settings
from dzhops.mysql import db_operate
from hostlist.models import HostList, Dzhuser, DataCenter, NetworkOperator, ProvinceArea, Catagory
from common.models import OperateRecord, ReturnRecord, DeployModules, ConfigUpdate, CommonOperate, ModulesLock
import time
import logging
import copy

# Import python libs
from numbers import Number
import re
import json


log = logging.getLogger('dzhops')

@login_required
def salt_key_list(request):
    """
    list all key
    """

    dccn_list = []
    user = request.user
    dc_hosts = {}
    dc_hosts_keys = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    minions,minions_pre,minions_rej = sapi.list_all_key()
    minions_set = set(minions)
    minions_pre_set = set(minions_pre)
    minions_rej_set = set(minions_rej)

    servers = DataCenter.objects.all()
    for server in servers:
        host_li = []
        hosts = HostList.objects.filter(dccn=server.dccn)
        dccn_list.append(server.dccn)
        for host in hosts:
            host_li.append(host.minionid)
        dc_hosts[server.dccn] = host_li

    for dc_h_k, dc_h_v in dc_hosts.iteritems():
        dc_hosts_keys[dc_h_k] = set(dc_h_v).intersection(minions_set)

    dccn_list.sort()

    return render_to_response(
        'salt_key_list.html',
        {'all_dc_list': dccn_list,
         'all_dc_hosts' : dc_hosts_keys
         },
        context_instance=RequestContext(request)
    )


def salt_accept_key(request):
    """
    accept salt minions key
    """

    node_name = request.GET.getlist('unacckeys')
    str_node_name = ','.join(node_name)
    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.accept_key(str_node_name)

    return HttpResponseRedirect(reverse('key_unaccept'))


def salt_delete_key(request):
    """
    delete salt minions key
    """

    node_name = request.GET.getlist('reacckeys')
    str_node_name = ','.join(node_name)

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.delete_key(str_node_name)

    return HttpResponseRedirect(reverse('key_list'))

def rejDeleteKey(request):
    '''
    Delete reject keys;
    :param request:
    :return:
    '''

    node_name = request.GET.getlist('rejectkeys')
    str_node_name = ','.join(node_name)

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    ret = sapi.delete_key(str_node_name)

    return HttpResponseRedirect(reverse('key_reject'))

@login_required
def salt_key_reject(request):
    """
    list rejected keys
    """
    user = request.user
    dccn_list = []
    dc_hosts = {}
    dc_hosts_keys = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    minions,minions_pre,minions_rej = sapi.list_all_key()
    minions_rej_set = set(minions_rej)

    servers = DataCenter.objects.all()
    for server in servers:
        host_li = []
        hosts = HostList.objects.filter(dccn=server.dccn)
        dccn_list.append(server.dccn)
        for host in hosts:
            host_li.append(host.minionid)
        dc_hosts[server.dccn] = host_li

    for dc_h_k, dc_h_v in dc_hosts.iteritems():
        dc_hosts_keys[dc_h_k] = set(dc_h_v).intersection(minions_rej_set)

    dccn_list.sort()

    return render_to_response(
        'salt_key_reject.html',
        {'all_dc_list': dccn_list,
         'all_minions_rej' : dc_hosts_keys},
        context_instance=RequestContext(request)
    )

@login_required
def salt_key_unaccept(request):
    """
    list unaccepted keys
    """
    user = request.user
    dccn_list = []
    dc_hosts = {}
    dc_hosts_keys = {}

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])
    minions,minions_pre,minions_rej = sapi.list_all_key()
    minions_pre_set = set(minions_pre)

    servers = DataCenter.objects.all()
    for server in servers:
        host_li = []
        hosts = HostList.objects.filter(dccn=server.dccn)
        dccn_list.append(server.dccn)
        for host in hosts:
            host_li.append(host.minionid)
        dc_hosts[server.dccn] = host_li

    for dc_h_k, dc_h_v in dc_hosts.iteritems():
        dc_hosts_keys[dc_h_k] = set(dc_h_v).intersection(minions_pre_set)

    dccn_list.sort()

    return render_to_response(
        'salt_key_unaccept.html',
        {'all_dc_list': dccn_list,'all_minions_pre': dc_hosts_keys },
        context_instance=RequestContext(request)
    )


def moduleDetection(module, user):
    '''
    Check whether the module is being used.
    :param module: 'cmd.run' or other module
    :param user: 'zhaogb' or other username
    :return: str or None, str for example: "zhaogb is using cmd.run"
    '''
    log.debug('%s detection module %s occupied' % (user, module))
    try:
        module_exist = ModulesLock.objects.get(module=module)
        module_status = module_exist.status
        module_user = module_exist.user
        if module_status == 'True':
            status = '%s is using module %s' % (module_user, module)
            log.info(status)
        elif module_status == 'False':
            status = ''
            log.info("Nobody uses module %s" % module)
        else:
            pass
    except ModulesLock.DoesNotExist:
        status = ''
        log.info("The %s module has never been used" % module)

    return status

def moduleLock(module, user):
    '''
    the module lock.
    :return:
    '''
    log.debug('%s Lock Module : %s' % (user,module))
    try:
        module_exist = ModulesLock.objects.get(module=module)
        module_status = module_exist.status
        if module_status == 'False':
            module_exist.status = 'True'
            module_exist.user = user
            module_exist.save()
            log.info("%s Lock Module %s Successed!" % (user, module))
        else:
            log.info("Someone could use this module %s" % module)
    except ModulesLock.DoesNotExist:
        log.info("The %s module has never been used" % module)
        module_lock = ModulesLock.objects.create(module=module, status='True', user=user)
        log.info("%s Lock Module %s Successed!" % (user, module))


def moduleUnlock(module, user):
    '''

    :return:
    '''
    log.debug('%s Unlock Module %s' % (user, module))
    module_unlock = ModulesLock.objects.get(module=module)
    module_unlock.status = 'False'
    module_unlock.user = ''
    module_unlock.save()
    log.info('%s unlock module %s successed!' % (user, module))


def datacenterToMinionID(datacenter_list):
    '''
    DataCenter list to minion id list;
    **Warning**: **Do not judge whether the list is empty!**
    :param dc_list: ['dctest1', 'dctest2', 'dctest3', ...] or ['*']
    :return: a set, ('zhaogb-201', 'zhaogb-202', 'zhaogb-203', ..., 'zhaogb-nnn')
    '''
    all_mininon_id_list = []
    if '*' in datacenter_list:
        result_data = HostList.objects.all().values_list("minionid")
        for row_data in result_data:
            minion_id = row_data[0]
            all_mininon_id_list.append(minion_id)
    else:
        for dc in datacenter_list:
            result_data_dccn = DataCenter.objects.get(dcen=dc)
            result_data_hosts = HostList.objects.filter(dccn=result_data_dccn.dccn)
            for row_data in result_data_hosts:
                minion_id = row_data.minionid
                all_mininon_id_list.append(minion_id)

    minion_id_set = set(all_mininon_id_list)

    return minion_id_set


def targetToMinionID(tgt):
    '''
    target host to minion id(str -> set);
    :param tgt: 'zhaogb-201, zhaogb-203,...' or 'zhaogb-*' or 'zh*' or '10.15.*' or 'z*,10*' or '*';
    :return:1.if * in tgt,return a set include all minion id;
            2.if 'zhaogb-*' or '10.10.* 'in tgt, return all server minion id for pattern prefix;
    '''

    target_list = tgt.split(',')
    minion_id_list = []
    all_minion_ip_list = []
    all_minion_id_list = []
    minion_ip_to_id_list = []
    minion_id_to_id_list = []

    if '*' in target_list:
        result_data = HostList.objects.all().values_list("minionid")
        for row_data in result_data:
            minion_id = row_data[0]
            minion_id_list.append(minion_id)
        minion_id_set = set(minion_id_list)
    else:
        all_minion_info_data = HostList.objects.all()
        for minion_info in all_minion_info_data:
            all_minion_ip_list.append(minion_info.ip)
            all_minion_id_list.append(minion_info.minionid)

        for target in target_list:
            target_replace_point = target.replace('.','\.')
            target_replace_star = target_replace_point.replace('*','.*')
            target_string = r'%s' % target_replace_star
            pattern = re.compile(target_string)
            for minion_ip in all_minion_ip_list:
                match_ip = pattern.match(minion_ip)
                if match_ip:
                    mtach_minion_ip_data = HostList.objects.get(ip=minion_ip)
                    match_minion_ip_to_id = mtach_minion_ip_data.minionid
                    minion_ip_to_id_list.append(match_minion_ip_to_id)
            for minion_id in all_minion_id_list:
                match_id = pattern.match(minion_id)
                if match_id:
                    minion_id_to_id_list.append(minion_id)

        minion_ip_to_id_set = set(minion_ip_to_id_list)
        minion_id_to_id_set = set(minion_id_to_id_list)
        minion_id_set = minion_ip_to_id_set.union(minion_id_to_id_set)

    return minion_id_set


def findJob(minionids_set,jid):
    '''

    :return:
    '''
    target_list_to_str = ','.join(list(minionids_set))
    log.debug('%s' % str(target_list_to_str))
    fun = 'saltutil.find_job'
    error_tolerant = 0.1
    loop = True

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])

    while loop:
        log.debug('into loop start')
        time.sleep(60)
        find_job_result = sapi.masterToMinionContent(target_list_to_str,fun,jid)
        log.error('%s' % str(find_job_result))
        if find_job_result is not None:
            find_job_result_keys = find_job_result.keys()
            num_keys = len(find_job_result_keys)
            log.error('find_job_result_keys: %d' % num_keys)
            num_minion = len(minionids_set)
            log.error('minion_set: %d' % num_minion)

            quantity_keys = len(find_job_result_keys)
            quantity_mini_id = len(minionids_set)
            quantity_error_tolerant = quantity_mini_id * error_tolerant
            quantity_unreturn = quantity_mini_id - quantity_keys

            if quantity_keys == quantity_mini_id:
                finished = []
                unfinished = []
                for key, value in find_job_result.iteritems():
                    log.debug('key: %s ;value: %s' % (key,value))
                    if value:
                        unfinished.append(key)
                        log.debug('unfinished: %s' % str(unfinished))
                    else:
                        finished.append(key)
                        log.debug('finished: %s' % str(finished))
                if len(unfinished) == 0:
                    loop = False
                    log.debug('views:308L %s' % loop)
                else:
                    continue
            elif quantity_unreturn <= quantity_error_tolerant:
                log.debug('unretunrn: %d;error_tolerant: %d' % (quantity_unreturn,quantity_error_tolerant))
                loop = False
            else:
                continue
        else:
            continue

    return loop

def outFormat(result):
    '''
    format out to screen;
    :param result:
        #result = {
        # 'zhaogb-201':
        #   {'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed':
        #       {'comment': 'zhaogb-201', 'name': '/usr/lib64/libodbc.so.1',
        #           'start_time': 'zhaogb-201',
        #           'result': True,
        #           'duration': 'zhaogb-201',
        #           '__run_num__': 2,
        #           'changes': {}
        #       }
        #   },
        # 'zhaogb-202':
        #    {'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed':
        #       {'comment': 'zhaogb-202',
        #           'name': 'zhaogb-202',
        #           'start_time': 'zhaogb-202',
        #           'result': True,
        #           'duration': 'zhaogb-202',
        #           '__run_num__': 2,
        #           'changes':
        #               {'diff': 'New file',
        #               'mode': '0644'
        #               }
        #       }
        #    }
        # }
    :return: colour is str 'True' or 'False', longstrva is a long formated strings;
    '''
    hostfa = 0
    hosttr = 0
    unret = {}

    for ka,va in result.iteritems():
        # result {'zhaogb-201':{},'zhaobg-202':{}}
        # ka zhaogb-201,zhaogb-202
        # va {'mo_watch':{'comment':'','result':'',...}}
        valcon = {}
        longstrva = ''
        falseStatus = 0
        trueStatus = 0
        liv = []

        minion_data = HostList.objects.get(minionid=ka)
        minion_ip = minion_data.ip

        if isinstance(va, dict):
            for kva in va.keys():
                # kva mo_watch,...
                liva = kva.split('_|-')
                liv.append(va[kva]['result'])

                if va[kva]['changes']:
                    changesStr = ''
                    if liva[0] == 'file':
                        if va[kva]['changes'].keys():
                            if ('diff' in va[kva]['changes'].keys()
                                    and va[kva]['changes']['diff'] != ''):
                                changesStr += u'\n\t对比 : \n\t\t{0}'.format(
                                        va[kva]['changes']['diff'])
                            if ('mode' in va[kva]['changes'].keys()
                                    and va[kva]['changes']['mode'] != ''):
                                changesStr += u'\n\t权限 : \n\t\t{0}'.format(
                                        va[kva]['changes']['mode'])
                            if ('diff' not in va[kva]['changes'].keys()
                                    and 'mode' not in va[kva]['changes'].keys()):
                                for ck,cv in va[kva]['changes'].iteritems():
                                    changesStr += u'\n\t{0}'.format(ck)
                                    if ('diff' in va[kva]['changes'][ck].keys()
                                            and va[kva]['changes'][ck]['diff'] != ''):
                                        changesStr += u'\n\t\t对比 : \n\t\t\t{0}'.format(cv['diff'])
                                    if ('mode' in va[kva]['changes'][ck].keys()
                                            and va[kva]['changes'][ck]['mode'] != ''):
                                        changesStr += u'\n\t\t权限 : \n\t\t\t{0}'.format(cv['mode'])

                    elif liva[0] == 'cmd':
                        if ('pid' in va[kva]['changes'].keys()
                                and va[kva]['changes']['pid'] != ''):
                            changesStr += u'\n\tPID : {0}'.format(va[kva]['changes']['pid'])
                        if ('retcode' in va[kva]['changes'].keys()
                                and va[kva]['changes']['retcode'] != ''):
                            changesStr += u'\n\t返回代码 : {0}'.format(va[kva]['changes']['retcode'])
                        if ('stderr' in va[kva]['changes'].keys()
                                and va[kva]['changes']['stderr'] != ''):
                            changesStr += u'\n\t错误 : {0}'.format(va[kva]['changes']['stderr'])
                        if ('stdout' in va[kva]['changes'].keys()
                                and va[kva]['changes']['stdout'] != ''):
                            changesStr += u'\n\t输出 : {0}'.format(va[kva]['changes']['stdout'])
                    else:
                        pass
                    va[kva]['changes'] = changesStr.encode('utf8')
                else:
                    pass

                strva = '结果 : {0}\n标签 : {1}\n操作 : {2}\n开始 : {3}\n耗时 : {4} ms\n变动 : {5}\n{6}\n'.format(
                    va[kva]['result'],
                    liva[1],
                    va[kva]['comment'],
                    va[kva]['start_time'],
                    va[kva]['duration'],
                    va[kva]['changes'],
                    '-'*60)
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
            unret[minion_ip] = valcon
        else:
            valcon['status'] = 'False'
            valcon['cont'] = str(va)
            unret[minion_ip] = valcon

    return unret, hostfa, hosttr

@login_required
def module_deploy(request):
    """
    deploy (mobile/manager/info..) module
    out  ret:{'host1':{'cont':'format result','status': colour },...} ,
                hostsft:{'sum':'','rsum':'','unre':'','unrestr':'','fa':'','tr':''}
    """

    user = request.user
    result = ''
    ret = {}
    hostsft = {}
    dcen_list = []
    data_centers = {}
    get_errors = []
    errors = []
    sls_list = []
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = DeployModules.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)

    if request.method == 'POST':
        check_tgt  = request.POST.get('tgt', '')
        check_dc_list = request.POST.get('datacenter', '')
        module_detection = moduleDetection('state.sls', user)
        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not request.POST.get('module', ''):
            get_errors.append(u'请选择将要安装的模块！')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
        else:
            tgt = request.POST.get('tgt')
            dc_list = request.POST.getlist('datacenter')
            arg = request.POST.get('module')
            module_lock = moduleLock('state.sls', user)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc_list:
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])
                tgt_list = tgt.split(',')
                if ('*' in tgt_list) or ('*' in dc_list):
                    jid = sapi.async_deploy_all(arg)
                else:
                    tgt_list_to_str = ','.join(all_minion_id_set)
                    jid = sapi.async_deploy(tgt_list_to_str,arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = tgt_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set,jid)

                db = db_operate()
                time.sleep(30)
                sql = 'select id,`return` from salt_returns where jid=%s'
                result = db.select_table(settings.RETURNS_MYSQL,sql,str(jid))

                hostsum = len(all_minion_id_set)
                sumset = all_minion_id_set

                hostrsum = len(result)
                returnset = set(result.keys())
                ret, hostfa, hosttr = outFormat(result)

                diffset = sumset.difference(returnset)
                hostunre = len(diffset)
                hostunrestr = ','.join(list(diffset))

                hostsft['sum'] = hostsum
                hostsft['rsum'] = hostrsum
                hostsft['unre'] = hostunre
                hostsft['unrestr'] = hostunrestr
                hostsft['fa'] = hostfa
                hostsft['tr'] = hosttr

                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=hostsum,
                    tgt_ret=hostrsum,
                    tgt_succ=hosttr,
                    tgt_fail=hostfa,
                    tgt_unret=hostunre,
                    tgt_unret_list=hostunrestr
                )

                module_unlock = moduleUnlock('state.sls', user)
            else:
                tips = u'请输入正确的服务器IP或MinionID'
                errors.append(tips.encode('utf-8'))

    return render_to_response(
        'salt_module_deploy.html',
        {'ret': ret,
         'hostsft': hostsft,
         'dcen_list': dcen_list,
         'data_centers': data_centers,
         'sls_list': sls_list,
         'sls_mod_dict': sls_mod_dict,
         'errors': errors
         },
        context_instance=RequestContext(request)
    )

@login_required
def module_update(request):
    """
    update (mobile/class/prog..etc) module
    out  {'host1':{'cont':'format result','status': colour },...}
    """

    user = request.user
    result = ''
    ret = {}
    hostsft = {}
    dcen_list = []
    data_centers = {}
    get_errors = []
    errors = []
    sls_list = []
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = ConfigUpdate.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)

    if request.method == 'POST':
        check_tgt  = request.POST.get('tgt', '')
        check_dc_list = request.POST.get('datacenter', '')
        module_detection = moduleDetection('state.sls', user)
        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not request.POST.get('module', ''):
            get_errors.append(u'请选择将要安装的模块！')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
        else:
            tgt = request.POST.get('tgt')
            dc_list = request.POST.getlist('datacenter')
            arg = request.POST.get('module')
            module_lock = moduleLock('state.sls', user)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc_list:
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])
                tgt_list = tgt.split(',')
                if ('*' in tgt_list) or ('*' in dc_list):
                    jid = sapi.async_deploy_all(arg)
                else:
                    tgt_list_to_str = ','.join(all_minion_id_set)
                    jid = sapi.async_deploy(tgt_list_to_str,arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = tgt_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set,jid)

                db = db_operate()
                time.sleep(30)
                sql = 'select id,`return` from salt_returns where jid=%s'
                result = db.select_table(settings.RETURNS_MYSQL,sql,str(jid))

                hostsum = len(all_minion_id_set)
                sumset = all_minion_id_set

                hostrsum = len(result)
                returnset = set(result.keys())
                ret, hostfa, hosttr = outFormat(result)

                diffset = sumset.difference(returnset)
                hostunre = len(diffset)
                hostunrestr = ','.join(list(diffset))

                hostsft['sum'] = hostsum
                hostsft['rsum'] = hostrsum
                hostsft['unre'] = hostunre
                hostsft['unrestr'] = hostunrestr
                hostsft['fa'] = hostfa
                hostsft['tr'] = hosttr

                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=hostsum,
                    tgt_ret=hostrsum,
                    tgt_succ=hosttr,
                    tgt_fail=hostfa,
                    tgt_unret=hostunre,
                    tgt_unret_list=hostunrestr
                )
                module_unlock = moduleUnlock('state.sls', user)
            else:
                tips = u'请输入正确的服务器IP或MinionID'
                errors.append(tips.encode('utf-8'))

    return render_to_response(
        'salt_module_update.html',
        {'ret': ret,
         'hostsft': hostsft,
         'dcen_list': dcen_list,
         'data_centers': data_centers,
         'sls_list': sls_list,
         'sls_mod_dict': sls_mod_dict,
         'errors': errors
         },
        context_instance=RequestContext(request)
    )

@login_required
def routine_maintenance(request):
    """
    routine maintenance
    out  {'host1':{'cont':'format result','status': colour },...}
    """

    user = request.user
    result = ''
    ret = {}
    hostsft = {}
    dcen_list = []
    data_centers = {}
    get_errors = []
    errors = []
    sls_list = []
    sls_mod_dict = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    result_sls = CommonOperate.objects.all()
    for row_data in result_sls:
        sls_mod_dict[row_data.slsfile] = row_data.module
        sls_list.append(row_data.slsfile)

    if request.method == 'POST':
        check_tgt  = request.POST.get('tgt', '')
        check_dc_list = request.POST.get('datacenter', '')
        module_detection = moduleDetection('state.sls', user)
        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not request.POST.get('module', ''):
            get_errors.append(u'请选择将要安装的模块！')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
        else:
            tgt = request.POST.get('tgt')
            dc_list = request.POST.getlist('datacenter')
            arg = request.POST.get('module')
            module_lock = moduleLock('state.sls', user)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc_list:
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])
                tgt_list = tgt.split(',')
                if ('*' in tgt_list) or ('*' in dc_list):
                    jid = sapi.async_deploy_all(arg)
                else:
                    tgt_list_to_str = ','.join(all_minion_id_set)
                    jid = sapi.async_deploy(tgt_list_to_str,arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = tgt_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set,jid)

                db = db_operate()
                time.sleep(30)
                sql = 'select id,`return` from salt_returns where jid=%s'
                result = db.select_table(settings.RETURNS_MYSQL,sql,str(jid))

                hostsum = len(all_minion_id_set)
                sumset = all_minion_id_set

                hostrsum = len(result)
                returnset = set(result.keys())
                ret, hostfa, hosttr = outFormat(result)

                diffset = sumset.difference(returnset)
                hostunre = len(diffset)
                hostunrestr = ','.join(list(diffset))

                hostsft['sum'] = hostsum
                hostsft['rsum'] = hostrsum
                hostsft['unre'] = hostunre
                hostsft['unrestr'] = hostunrestr
                hostsft['fa'] = hostfa
                hostsft['tr'] = hosttr

                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=hostsum,
                    tgt_ret=hostrsum,
                    tgt_succ=hosttr,
                    tgt_fail=hostfa,
                    tgt_unret=hostunre,
                    tgt_unret_list=hostunrestr
                )
                module_unlock = moduleUnlock('state.sls', user)
            else:
                tips = u'请输入正确的服务器IP或MinionID'
                errors.append(tips.encode('utf-8'))

    return render_to_response(
        'salt_routine_maintenance.html',
        {'ret': ret,
         'hostsft': hostsft,
         'dcen_list': dcen_list,
         'data_centers': data_centers,
         'sls_list': sls_list,
         'sls_mod_dict': sls_mod_dict,
         'errors': errors
         },
        context_instance=RequestContext(request)
    )

@login_required
def remote_execution(request):
    """
    remote command execution
    out(type:string)    ret = 'format string'
    """

    user = request.user.username
    ret = ''
    tret = ''
    hostsft = {}
    dcen_list = []
    data_centers = {}
    get_errors = []
    errors = []
    danger_cmd = ('rm','reboot','init','shutdown','poweroff')
    minion_ip_list = []

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    if request.method == 'POST':
        check_tgt  = request.POST.get('tgt', '')
        check_dc_list = request.POST.get('datacenter', '')
        module_detection = moduleDetection('cmd.run', user)
        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not request.POST.get('arg', ''):
            get_errors.append(u'请输入将要执行的命令！')
        else:
            arg_string = request.POST.get('arg')
            arg_strip = arg_string.strip()
            arg_list = arg_strip.split()
            arg_one = arg_list[0]
            for dcmd in danger_cmd:
                if arg_one == dcmd:
                    get_errors.append(u'%s 命令危险，不允许使用！' % arg_one)

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
        else:
            tgt = request.POST.get('tgt')
            dc_list = request.POST.getlist('datacenter')
            arg = request.POST.get('arg')
            module_lock = moduleLock('cmd.run', user)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc_list:
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])
                tgt_list = tgt.split(',')
                if ('*' in tgt_list) or ('*' in dc_list):
                    unret = sapi.remote_execution(arg)
                else:
                    tgt_list_to_str = ','.join(all_minion_id_set)
                    unret = sapi.list_remote_execution(tgt_list_to_str, arg)

                hostsum = len(all_minion_id_set)
                sumset = all_minion_id_set
                ret_list = unret.keys()
                hostrsum = len(ret_list)
                returnset = set(ret_list)

                diffset = sumset.difference(returnset)
                hostunre = len(diffset)
                hostunrestr = ','.join(list(diffset))

                hostsft['sum'] = hostsum
                hostsft['rsum'] = hostrsum
                hostsft['unre'] = hostunre
                hostsft['unrestr'] = hostunrestr

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    tgtlist = tgt.split(',')
                    operate_tgt = tgtlist[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p3 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt)

                for kret in unret.keys():
                    minion_data = HostList.objects.get(minionid=kret)
                    log.debug('remote_exec: %s' % str(kret))
                    minion_ip = minion_data.ip
                    minion_ip_list.append(minion_ip)
                    minion_ip_list.sort()
                for mip in minion_ip_list:
                    minion_data = HostList.objects.get(ip=mip)
                    kret = minion_data.minionid
                    lret = mip + ':\n' + unret[kret] + '\n'
                    tret += lret + '\n'
                ret = tret

                saveRecord = ReturnRecord.objects.create(
                    #jid=jid[0],
                    jid='',
                    tgt_total=hostsum,
                    tgt_ret=hostrsum,
                    tgt_unret=hostunre,
                    tgt_unret_list=hostunrestr
                )

                module_unlock = moduleUnlock('cmd.run', user)
            else:
                tips = u'请输入正确的服务器IP或MinionID'
                errors.append(tips.encode('utf-8'))

    return render_to_response(
        'salt_remote_execution.html',
        {'ret': ret,
         'hostsft': hostsft,
         'dcen_list': dcen_list,
         'data_centers': data_centers,
         'errors': errors
         },
        context_instance=RequestContext(request)
    )


@login_required
def record(request):

    user = request.user
    page_size = 10

    all_record = OperateRecord.objects.order_by('-id')
    paginator = Paginator(all_record, page_size)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    #page_id = range(((page-1)*13+1),(page*13+1))

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response(
        'common_record.html',
        {'posts': posts,
         #'page_id': page_id,
        },
        context_instance=RequestContext(request)
    )

@login_required
def recordDetail(request):

    user = request.user
    hostsft = {}

    if 'jid' in request.GET:
        job_id = request.GET.get('jid')
        jid_record = OperateRecord.objects.get(jid=job_id)

        try:
            jidStatus = ReturnRecord.objects.get(jid=job_id)
            hostsft['sum'] = jidStatus.tgt_total
            hostsft['rsum'] = jidStatus.tgt_ret
            hostsft['unre'] = jidStatus.tgt_unret
            hostsft['unrestr'] = jidStatus.tgt_unret_list
            hostsft['fa'] = jidStatus.tgt_fail
            hostsft['tr'] = jidStatus.tgt_succ
        except:
            hostsft['sum'] = 'Null'
            hostsft['rsum'] = 'Null'
            hostsft['unre'] = 'Null'
            hostsft['unrestr'] = 'Null'
            hostsft['fa'] = 'Null'
            hostsft['tr'] = 'Null'

        db = db_operate()
        sql = 'select id,`return` from salt_returns where jid=%s'
        jid_result = db.select_table(settings.RETURNS_MYSQL,sql,str(job_id))
        ret, hostfa, hosttr = outFormat(jid_result)

    else:
        jid_record = ''
        ret = {}

    return render_to_response(
        'common_record_detail.html',
        {'jid_record': jid_record,
         'hostsft': hostsft,
         'ret': ret
        },
        context_instance=RequestContext(request)
    )

@login_required
def hostDataCollection(request):
    '''
    The Servers data collection;
    :param request:
    :return:
    '''

    user = request.user
    data_centers = {}
    dcen_list = []

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    return render_to_response(
        'host_data_coll.html',
        {'dcen_list': dcen_list,
         'data_centers': data_centers,
        },
        context_instance=RequestContext(request)
    )

@login_required
def dataCollection(request):
    '''
    The Servers data collection;
    :param request:
    :return:
    '''

    user = request.user
    fun = 'grains.item'
    arg_ip = 'ip4_interfaces'
    arg_id = 'id'
    arg_host = 'localhost'
    minion_info = {}
    errors = ''

    if request.method == 'GET':
        if not request.GET.get('datacenter',''):
            errors.append('xxx')

    if not errors:
        datacenter = request.GET.get('datacenter')
        tgt = '*_*_*_%s_*' % datacenter
        sapi = SaltAPI(
            url = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
        )

        minion_ip_return = sapi.masterToMinion(tgt,fun,arg_ip)
        minion_id_return = sapi.masterToMinion(tgt,fun,arg_id)
        minion_host_return = sapi.masterToMinion(tgt,fun,arg_host)
        minion_ip_dict = minion_ip_return['return'][0]
        minion_id_dict = minion_id_return['return'][0]
        minion_host_dict = minion_host_return['return'][0]
        minion_keys_list = minion_ip_dict.keys()
        minion_sum = len(minion_keys_list)
        minion_keys_list.sort()
        for mini_key in minion_keys_list:
            minion_info_list = []
            minion_info_list.append(minion_ip_dict[mini_key]['ip4_interfaces']['eth0'][0])
            minion_info_list.append(minion_host_dict[mini_key]['localhost'])
            minion_id = minion_id_dict[mini_key]['id']
            minion_info_list.append(minion_id)

            minion_id_split = minion_id.split('_')
            # CNET_HQ_ZJ_WZ_61_164_153_56
            minion_id_noen = minion_id_split[0]
            minion_id_catagoryen = minion_id_split[1]
            minion_id_paen = minion_id_split[2]
            minion_id_dcen = minion_id_split[3]

            minion_id_networkoperator = NetworkOperator.objects.get(noen=minion_id_noen)
            minion_id_nocn = minion_id_networkoperator.nocn
            minion_info_list.append(minion_id_nocn)

            minion_id_catagory = Catagory.objects.get(catagoryen=minion_id_catagoryen)
            minion_id_catagorycn = minion_id_catagory.catagorycn
            minion_info_list.append(minion_id_catagorycn)

            minion_id_provincearea = ProvinceArea.objects.get(paen=minion_id_paen)
            minion_id_pacn = minion_id_provincearea.pacn
            minion_info_list.append(minion_id_pacn)

            minion_id_datacenter = DataCenter.objects.get(dcen=minion_id_dcen)
            minion_id_dccn = minion_id_datacenter.dccn
            minion_info_list.append(minion_id_dccn)

            minion_info_tuple = tuple(minion_info_list)
            minion_info[mini_key] = minion_info_tuple

        for mininfo_key,mininfo_data in minion_info.iteritems():
            h = HostList.objects.create(
                ip=mininfo_data[0],
                hostname=mininfo_data[1],
                minionid=mininfo_data[2],
                nocn=mininfo_data[3],
                catagorycn=mininfo_data[4],
                pacn=mininfo_data[5],
                dccn=mininfo_data[6]
            )

    return render_to_response(
        'common_data_collection.html',
        {'minion_sum' : minion_sum,
         'minion_keys_list': minion_keys_list,
         'minion_info_dict': minion_info,
        },
        context_instance=RequestContext(request)
    )

