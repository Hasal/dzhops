# -*- coding: utf-8 -*-

from hostlist.models import HostList, DataCenter
from saltstack.models import SaltReturns
from saltstack.models import ModulesLock
from saltstack.saltapi import SaltAPI
from dzhops import settings

import logging, time, json, re

log = logging.getLogger('dzhops')

def moduleDetection(module, user):
    '''
    检测如state.sls/cmd.run等模块是否被占用；
    :param module: 'cmd.run' 或 'state.sls'
    :param user: 'zhaogb' 或其他用户名；
    :return: 如果模块被占用，则返回如 "zhaogb is using cmd.run"；如果模块没有被占用，则返回空字符串；
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
    将模块锁定；
    :param module: 'cmd.run' 或 'state.sls'
    :param user: 'zhaogb' 或其他用户名；
    :return: None
    '''
    log.debug('%s Lock Module : %s' % (user, module))
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
    将锁定的模块解锁；
    :param module: 'cmd.run' 或 'state.sls'
    :param user: 'zhaogb' 或其他用户名；
    :return: None
    '''
    log.debug('%s Unlock Module %s' % (user, module))
    module_unlock = ModulesLock.objects.get(module=module)
    module_unlock.status = 'False'
    module_unlock.user = ''
    module_unlock.save()
    log.info('%s unlock module %s successed!' % (user, module))

def targetToMinionID(tgt):
    '''
    将服务器IP或MinionID字符串转换成由MinionID组成的集合；
    如果传过来‘*’，会返回全部MinionKeys组成的列表，将用于计算目标主机数量；
    :param tgt: 'zhaogb-201, zhaogb-203,...' or 'zhaogb-*' or 'zh*' or '10.15.*' or 'z*,10*' or '*';
    :return:1.如果‘*’在tgt中，则返回全部MinionKeys组成的列表;
            2.如果'zhaogb-*' or '10.10.* '在tgt中, 返回转换、正则匹配到的相关minionid集合;
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
            if '*' in target:
                target_replace_point = target.replace('.', '\.')
                target_replace_star = target_replace_point.replace('*', '.*')
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
            else:
                target_replace_none = target.replace('.','')
                if target_replace_none.isdigit():
                    try:
                        mtach_minion_ip_data = HostList.objects.get(ip=target)
                        match_minion_ip_to_id = mtach_minion_ip_data.minionid
                        minion_ip_to_id_list.append(match_minion_ip_to_id)
                    except HostList.DoesNotExist:
                        log.error('Without this IP on host list. IP:{0}'.format(target))
                else:
                    try:
                        mtach_minion_id_data = HostList.objects.get(minionid=target)
                        minion_ip_to_id_list.append(target)
                    except HostList.DoesNotExist:
                        log.error("MinionID don't exsit. Minion id:{0}".format(target))

        minion_ip_to_id_set = set(minion_ip_to_id_list)
        minion_id_to_id_set = set(minion_id_to_id_list)
        minion_id_set = minion_ip_to_id_set.union(minion_id_to_id_set)

    return minion_id_set

def datacenterToMinionID(datacenter_list):
    '''
    由机房名称组成的列表转换成由MinionID组成的集合；
    如果传过来‘*’，会返回全部MinionKeys组成的列表，将用于计算目标主机数量；
    **注意**: **这里没有判断传过来的列表是否为空，请调用该函数之前自己判断**
    :param dc_list: ['dctest1', 'dctest2', 'dctest3', ...] or ['*']
    :return: a set, set(['zhaogb-201', 'zhaogb-202', 'zhaogb-203', ..., 'zhaogb-nnn'])
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

def findJob(minionids_set, jid):
    '''

    :return:
    '''
    target_list_to_str = ','.join(list(minionids_set))
    log.debug('target_list: %s' % str(target_list_to_str))
    fun = 'saltutil.find_job'
    diff_send_receive = []
    loop = True

    sapi = SaltAPI(
        url=settings.SALT_API['url'],
        username=settings.SALT_API['user'],
        password=settings.SALT_API['password'])

    while loop:
        counter = 0
        # log.debug('The loop variable')
        log.debug('into loop start [common.views.findJob]')
        time.sleep(10)
        find_job_result = sapi.masterToMinionContent(target_list_to_str, fun, jid)
        log.debug('find_job_result: %s' % str(find_job_result))
        find_job_result_set = set(find_job_result.keys())
        diff_send_receive.extend(list(minionids_set.difference(find_job_result_set)))
        find_job_result_value = find_job_result.values()
        for eachDict in find_job_result_value:
            if eachDict:
                log.debug('The find job result is Dict, It is values list is Not null.')
                break
            else:
                counter += 1
        if counter == len(find_job_result_set):
            loop = False

    diff_send_receive_set = set(diff_send_receive)

    return diff_send_receive_set

def mysqlReturns(jid):
    '''

    :param jid: u'20160217142922771111'
    :return:{'host1':{'dict_content'},'host2':{'dict_content'},...}
    '''
    jid = jid.encode('utf-8')
    dict_result = {}
    try:
        log.debug('Query the database salt_returns for %s' % jid)
        return_data = SaltReturns.objects.filter(jid=jid)
        for row in return_data:
            data_return = json.loads(row.return_field)
            dict_result[row.id] = data_return
    except BaseException, e:
        log.error(str(e))

    return dict_result

def outFormat(result):
    '''
    将从数据中获取到的结果，进行格式化输出;
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
    :return: 多维列表，形如：[
                            [ip1', {'status': value1, 'cont': longstrings1}],
                            [ip2', {'status': value2, 'cont': longstrings2}],
                            ... ...
                           ]
    '''
    hostfa = 0
    hosttr = 0
    unret = {}

    for ka, va in result.iteritems():
        # result {'zhaogb-201':{},'zhaogb-202':{}}
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
                                for ck, cv in va[kva]['changes'].iteritems():
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
                    '-' * 60)
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

    # 结果排序工作改为由前端处理，此处注释
    # result_keys_list = unret.keys()
    # result_keys_list.sort()
    # log.debug('Result keys list sorted: {0}'.format(str(result_keys_list)))
    # for ip in result_keys_list:
    #     content = unret.get(ip)
    #     sub_list = [ip, content]
    #     result.append(sub_list)

    return unret, hostfa, hosttr

def manageResult(send_ids_set, recv_ips_list):
    '''
    计算目标客户端数量，回收结果数量，未返回结果的数量，未返回结果的IP列表；
    :param send_ids_set:
    :param recv_ips_list:
    :return: {digit, digit, digit, strings}
    '''
    diff_ip_list = []
    info_keys = ('send_count', 'recv_count', 'unrecv_count', 'unrecv_strings')
    send_ids_count = len(send_ids_set)
    recv_ips_count = len(recv_ips_list)
    if send_ids_count == recv_ips_count:
        info_values = [send_ids_count, recv_ips_count, 0, '']
        send_recv_info = dict(zip(info_keys, info_values))
    elif recv_ips_count == 0:
        unrecv_ip_list = []
        for i in send_ids_set:
            data = HostList.objects.get(minionid=i)
            unrecv_ip_list.append(data.ip)
        unrecv_strings = ', '.join(unrecv_ip_list)
        info_values = [send_ids_count, 0, send_ids_count, unrecv_strings]
        send_recv_info = dict(zip(info_keys, info_values))
    else:
        recv_ids_list = []
        for i in recv_ips_list:
            minion_data = HostList.objects.get(ip=i)
            minion_id = minion_data.minionid
            recv_ids_list.append(minion_id)
        recv_ids_set = set(recv_ids_list)
        diff_set = send_ids_set.difference(recv_ids_set)
        unrecv_count = len(diff_set)
        for i in diff_set:
            data = HostList.objects.get(minionid=i)
            diff_ip_list.append(data.ip)
        unrecv_strings = ', '.join(diff_ip_list)
        info_values = [send_ids_count, recv_ips_count, unrecv_count, unrecv_strings]
        send_recv_info = dict(zip(info_keys, info_values))
    return send_recv_info