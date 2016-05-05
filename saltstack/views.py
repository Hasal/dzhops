# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from hostlist.models import DataCenter
from record.models import OperateRecord, ReturnRecord
from saltstack.models import DangerCommand, DeployModules, ConfigUpdate, CommonOperate
from saltstack.saltapi import SaltAPI
from saltstack.util import targetToMinionID, datacenterToMinionID, findJob, mysqlReturns, outFormat, manageResult, \
    moduleDetection, moduleLock, moduleUnlock
from dzhops import settings

import logging, json, time, copy

# Create your views here.

log = logging.getLogger('dzhops')


@login_required
def deployProgram(request):
    '''
    部署程序，如部署行情程序、监控程序、账号代理程序等；
    :param request:
            目标Minions或机房、组；
            需要执行的sls文件
    :return:
            {'minion ip':{'cont':'format result','status': colour },...} ,
                hostsft:{'sum':'','rsum':'','unre':'','unrestr':'','fa':'','tr':''}
    '''
    user = request.user.username
    dcen_list = []
    sls_list = []
    data_centers = {}
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
    sls_list.sort()

    return render(
        request,
        'salt_deploy.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )

@login_required
def updateConfig(request):
    '''
    配置更新，如行情配置更新、class文件更新、ssh配置更新等；
    :param request:
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}
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
    sls_list.sort()

    return render(
        request,
        'salt_update.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )

@login_required
def routineMaintenance(request):
    '''
    日常维护操作，比如日志清理、批量重启程序等；
    :param request:
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}
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

    return render(
        request,
        'salt_routine.html',
        {
            'dcen_list': dcen_list,
            'data_centers': data_centers,
            'sls_list': sls_list,
            'sls_mod_dict': sls_mod_dict
        }
    )

@login_required
def deployProgramApi(request):
    '''
    模块部署功能，前端页面提交的数据由该函数处理，执行完毕后返回json格式数据到api；
    :param request:
    :return:
    '''
    user = request.user.username
    salt_module = 'state.sls'
    get_errors = []
    errors = []
    result_dict = {}

    if request.method == 'GET':
        check_tgt = request.GET.get('tgt', '')
        check_dc_list = request.GET.get('datacenter', '')
        check_arg = request.GET.get('sls', '')

        module_detection = moduleDetection(salt_module, user)

        if module_detection:
            get_errors.append(module_detection)
            log.debug('{0}'.format(str(module_detection)))
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要输入服务器IP或选择机房！')
            log.error('Did not enter servers ip or choose data center.')
        if not check_arg:
            get_errors.append(u'请选择将要进行的操作！')
            log.error('Not select the file of salt state.')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
            result_dict['errors'] = errors
        else:
            tgt = request.GET.get('tgt', '')
            dc = request.GET.get('datacenter', '')
            arg = request.GET.get('sls', '')

            dc_clean = dc.strip(',')
            log.debug(str(dc_clean))
            dc_list = dc_clean.split(',')
            target_list = tgt.split(',')
            tgt_mixture_list = copy.deepcopy(dc_list)
            tgt_mixture_list.extend(target_list)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc:
                log.debug(str(dc_list))
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)
            # log.debug('The all target minion id set: {0}'.format(str(all_minion_id_set)))

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])

                module_lock = moduleLock(salt_module, user)

                if '*' in tgt_mixture_list:
                    jid = sapi.asyncMasterToMinion('*', salt_module, arg)
                else:
                    tgt_list_to_str = ','.join(list(all_minion_id_set))
                    jid = sapi.asyncMasterToMinion(tgt_list_to_str, salt_module, arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = target_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set, jid)
                result = mysqlReturns(jid)
                module_unlock = moduleUnlock(salt_module, user)
                ret, hostfa, hosttr = outFormat(result)

                # log.debug(str(ret))
                recv_ips_list = ret.keys()
                send_recv_info = manageResult(all_minion_id_set, recv_ips_list)
                send_recv_info['succeed'] = hosttr
                send_recv_info['failed'] = hostfa
                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=send_recv_info['send_count'],
                    tgt_ret=send_recv_info['recv_count'],
                    tgt_succ=send_recv_info['succeed'],
                    tgt_fail=send_recv_info['failed'],
                    tgt_unret=send_recv_info['unrecv_count'],
                    tgt_unret_list=send_recv_info['unrecv_strings']
                )
                result_dict['result'] = ret
                result_dict['info'] = send_recv_info
            else:
                log.info('The all target minion id set is Null.')
                set_null = u'数据库中没有找到输入的主机，请确认输入是否正确！'
                result_dict['errors'] = set_null.encode('utf-8')
    ret_json = json.dumps(result_dict)

    return HttpResponse(ret_json, content_type='application/json')

@login_required
def remoteExecute(request):
    '''
    通过SaltStack cmd.run模块，对Salt minion远程执行命令；
    :param request: None
    :return:
    '''
    user = request.user.username
    dcen_list = []
    data_centers = {}

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dcen_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dcen_list.sort()

    return render(
        request,
        'salt_execute.html',
        {'dcen_list': dcen_list, 'data_centers': data_centers}
    )


@login_required
def remoteExecuteApi(request):
    '''
    远程执行的命令通过JQuery(ajax)提交到这里，处理后返回结果json;
    :param request:
    :return:
    '''
    user = request.user.username
    get_errors = []
    errors = []
    result_dict = {}
    danger_cmd_list = []

    danger_cmd_data = DangerCommand.objects.filter(status='True')
    if danger_cmd_data:
        for i in danger_cmd_data:
            danger_cmd_list.append(i.command)
    else:
        log.debug('The table of DangerCommand is Null.')

    if request.method == 'GET':
        check_tgt = request.GET.get('tgt', '')
        check_dc_list = request.GET.get('datacenter', '')
        check_arg = request.GET.get('arg', '')

        module_detection = moduleDetection('cmd.run', user)

        if module_detection:
            get_errors.append(module_detection)
        if not (check_tgt or check_dc_list):
            get_errors.append(u'需要指定目标主机或目标机房！')
        if not check_arg:
            get_errors.append(u'请输入将要执行的命令！')
        else:
            if danger_cmd_list:
                arg_list = check_arg.split(';')
                for i in arg_list:
                    try:
                        command = i.split()[0]
                    except IndexError, e:
                        log.debug('Command ends with a semicolon, Error info: {0}.'.format(str(e)))
                        continue
                    for j in danger_cmd_list:
                        if j in command:
                            get_errors.append(u'%s 命令危险，不允许使用！' % command)
            else:
                log.debug('Databases has not danger command')

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf-8'))
            result_dict['errors'] = errors
        else:
            tgt = request.GET.get('tgt', '')
            dc = request.GET.get('datacenter', '')
            arg = request.GET.get('arg', '')

            dc_clean = dc.strip(',')
            log.debug(str(dc_clean))
            dc_list = dc_clean.split(',')
            target_list = tgt.split(',')
            tgt_mixture_list = copy.deepcopy(dc_list)
            tgt_mixture_list.extend(target_list)

            if tgt:
                minion_id_from_tgt_set = targetToMinionID(tgt)
            else:
                minion_id_from_tgt_set = set([])
            if dc:
                log.debug(str(dc_list))
                minion_id_from_dc_set = datacenterToMinionID(dc_list)
            else:
                minion_id_from_dc_set = set([])
            all_minion_id_set = minion_id_from_tgt_set.union(minion_id_from_dc_set)
            log.debug('The all target minion id set: {0}'.format(str(all_minion_id_set)))

            if all_minion_id_set:
                sapi = SaltAPI(
                    url=settings.SALT_API['url'],
                    username=settings.SALT_API['user'],
                    password=settings.SALT_API['password'])

                module_lock = moduleLock('cmd.run', user)

                if '*' in tgt_mixture_list:
                    jid = sapi.asyncMasterToMinion('*', 'cmd.run', arg)
                else:
                    tgt_list_to_str = ','.join(list(all_minion_id_set))
                    jid = sapi.asyncMasterToMinion(tgt_list_to_str, 'cmd.run', arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = target_list[0]
                else:
                    operate_tgt = 'unknown'

                op_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                op_user = arg
                op_tgt = '%s...' % operate_tgt
                p1 = OperateRecord.objects.create(
                    nowtime=op_time,
                    username=user,
                    user_operate=op_user,
                    simple_tgt=op_tgt,
                    jid=jid)

                find_job = findJob(all_minion_id_set, jid)
                result = mysqlReturns(jid)
                module_unlock = moduleUnlock('cmd.run', user)
                ret, hostfa, hosttr = outFormat(result)

                # log.debug(str(ret))
                recv_ips_list = ret.keys()
                send_recv_info = manageResult(all_minion_id_set, recv_ips_list)
                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=send_recv_info['send_count'],
                    tgt_ret=send_recv_info['recv_count'],
                    tgt_unret=send_recv_info['unrecv_count'],
                    tgt_unret_list=send_recv_info['unrecv_strings']
                )
                result_dict['result'] = ret
                result_dict['info'] = send_recv_info
            else:
                log.info('The all target minion id set is Null.')
                set_null = u'数据库中没有找到输入的主机，请确认输入是否正确！'
                result_dict['errors'] = set_null.encode('utf-8')
    ret_json = json.dumps(result_dict)

    return HttpResponse(ret_json, content_type='application/json')
