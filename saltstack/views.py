# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from saltstack.saltapi import SaltAPI
from common.views import moduleDetection, moduleLock, moduleUnlock
from common.models import OperateRecord, ReturnRecord
from saltstack.util import targetToMinionID, datacenterToMinionID, findJob, mysqlReturns, outFormat, manageResult
from hostlist.models import DataCenter
from dzhops import settings

import logging, json, time, copy

# Create your views here.

log = logging.getLogger('dzhops')


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
    danger_cmd = ('rm', 'reboot', 'init', 'shutdown', 'poweroff')

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
            arg_list = check_arg.split(';')
            for i in arg_list:
                command = i.split()[0]
                if command in danger_cmd:
                    get_errors.append(u'%s 命令危险，不允许使用！' % command)

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

                # module_lock = moduleLock('cmd.run', user)

                if '*' in tgt_mixture_list:
                    jid = sapi.asyncMasterToMinion('*', 'cmd.run', arg)
                else:
                    tgt_list_to_str = ','.join(list(all_minion_id_set))
                    jid = sapi.asyncMasterToMinion(tgt_list_to_str, 'cmd.run', arg)

                if dc_list:
                    operate_tgt = dc_list[0]
                elif tgt:
                    operate_tgt = tgt_list[0]
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
                # module_unlock = moduleUnlock('cmd.run', user)
                ret, hostfa, hosttr = outFormat(result)

                # log.debug(str(ret))
                recv_ips_list = ret.keys()
                send_recv_info = manageResult(all_minion_id_set, recv_ips_list)
                saveRecord = ReturnRecord.objects.create(
                    jid=jid,
                    tgt_total=send_recv_info['send_count'],
                    tgt_ret=send_recv_info['recv_conut'],
                    tgt_unret=send_recv_info['unrecv_conut'],
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