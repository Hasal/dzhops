# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from replacedata.models import StockExchage
from hostlist.models import DataCenter
from record.models import OperateRecord, ReturnRecord
from saltstack.saltapi import SaltAPI
from saltstack.util import outFormat, datacenterToMinionID, findJob, mysqlReturns, manageResult, moduleDetection, moduleLock, moduleUnlock
from dzhops import settings

import os, time, logging, json

# Create your views here.
log = logging.getLogger('dzhops')

@login_required
def repairHistoryData(request):
    '''
    本功能最初设计目的是补错误的历史数据。
    :param request:
    :return:
    '''
    user = request.user.username
    dc_list = []
    data_centers = {}
    stock_exchanges = []

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dc_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dc_list.sort()

    result_stk = StockExchage.objects.all()
    for stkcode in result_stk:
        stock_exchanges.append(stkcode.stkexchen)

    return render(
        request,
        'repair_history_data.html',
        {
            'dc_list': dc_list,
            'data_centers': data_centers,
            'stock_exchanges': stock_exchanges
        }
    )

@login_required
def repairHistoryDataAPI(request):
    '''

    :param request:
    :return:
    '''
    user = request.user.username
    data_path = '/srv/salt/dzh_store/mobileserver/DATA/'
    state_module = 'state.sls'
    get_errors = []
    errors = []
    result_dict = {}

    if request.method == 'GET':
        module_detection = moduleDetection(state_module, user)
        if module_detection:
            get_errors.append(module_detection)
        if not request.GET.get('datacenter', ''):
            get_errors.append(u'需要指定目标机房，才能允许后续操作！')
        if not request.GET.get('stockexchange', ''):
            get_errors.append(u'亲，需要指定本次将要补数据的市场！')
        if not request.GET.get('sls', ''):
            get_errors.append(u'行情程序需要重启吗？请选择之一！')
        if not os.path.exists(data_path):
            get_errors.append(u'目录：{0} 不存在！'.format(data_path))
            log.error("The data path:{0} not exist.".format(data_path))

        if get_errors:
            for error in get_errors:
                errors.append(error.encode('utf8'))
            result_dict['errors'] = errors
        else:
            get_dc_str = request.GET.get('datacenter')
            get_exch_str = request.GET.get('stockexchange')
            get_sls = request.GET.get('sls')

            dc_clean = get_dc_str.strip(',')
            getdclist = dc_clean.split(',')
            exch_clean = get_exch_str.strip(',')
            getexchlist = exch_clean.split(',')
            getstatesls = get_sls

            if get_dc_str:
                result_host_set = datacenterToMinionID(getdclist)
            else:
                result_host_set = set([])

            stkexch_set = set(os.listdir(data_path))
            clear_dir = stkexch_set.difference(set(getexchlist))
            for exchcode in clear_dir:
                day_path = os.path.join(data_path, exchcode, 'history/day')
                day_files = os.listdir(day_path)
                if day_files:
                    for dyfile in day_files:
                        dyfile_path = os.path.join(day_path,dyfile)
                        os.remove(dyfile_path)
                    log.info('Delete Other Market Success')

            sapi = SaltAPI(
                url=settings.SALT_API['url'],
                username=settings.SALT_API['user'],
                password=settings.SALT_API['password'])

            module_lock = moduleLock(state_module, user)
            if '*' in getdclist:
                jid = sapi.asyncMasterToMinion(getstatesls)
            else:
                tgt_list_to_str = ','.join(list(result_host_set))
                jid = sapi.asyncMasterToMinion(tgt_list_to_str,getstatesls)
            module_unlock = moduleUnlock(state_module, user)

            if getexchlist:
                operate_tgt = getexchlist[0]
            else:
                operate_tgt = 'unknown'

            op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            op_user = getstatesls
            op_tgt = '%s...' % operate_tgt
            p1 = OperateRecord.objects.create(
                nowtime=op_time,
                username=user,
                user_operate=op_user,
                simple_tgt=op_tgt,
                jid=jid)

            find_job = findJob(result_host_set,jid)
            result = mysqlReturns(jid)

            ret, hostfa, hosttr = outFormat(result)

            recv_ips_list = ret.keys()
            send_recv_info = manageResult(result_host_set, recv_ips_list)
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
    ret_json = json.dumps(result_dict)

    return HttpResponse(ret_json, content_type='application/json')
