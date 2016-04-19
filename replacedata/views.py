# -*- coding: utf-8 -*-
# from django
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# from dzhops
from replacedata.models import StockExchage, StockIndex
from hostlist.models import HostList, Dzhuser, DataCenter
from common.models import OperateRecord, ReturnRecord, SaltReturns
from common.saltapi import SaltAPI
from dzhops import settings
from common.views import outFormat, datacenterToMinionID, findJob, mysqlReturns, moduleDetection, moduleLock, moduleUnlock
# from replacedata.forms import RedataAllForms

# Import python libs
import os, time, re, logging

# Create your views here.
log = logging.getLogger('dzhops')

@login_required
def dataReplaceHistory(request):
    '''
    Repalce data of all market history;
    :param request:
    :return:
    dc_list ['dctest1','dctest2','dctest3','dctest4']
    data_centers {'dctest1':'测试机房1','dctest2':'测试机房2',...}
    stock_exchanges ['SH','SZ','B$',....]
    '''

    user = request.user.username
    data_path = '/srv/salt/dzh_store/mobileserver/DATA/'
    dc_list = []
    data_centers = {}
    stock_exchanges = []
    ret = {}
    hostsft = {}
    judgerrors = []
    errors = []
    hostrsum = 0
    diff_ip_list = []

    result_dc = DataCenter.objects.all()
    for dc in result_dc:
        dc_list.append(dc.dcen)
        data_centers[dc.dcen] = dc.dccn
    dc_list.sort()

    result_stk = StockExchage.objects.all()
    for stkcode in result_stk:
        stock_exchanges.append(stkcode.stkexchen)

    if request.method == 'POST':
        module_detection = moduleDetection('state.sls', user)
        if module_detection:
            get_errors.append(module_detection)
        if not request.POST.get('datacenter', ''):
            judgerrors.append(u'需要指定目标机房，才能允许后续操作！')
        if not request.POST.get('stockexchange', ''):
            judgerrors.append(u'亲，需要指定本次将要补数据的市场！')
        if not request.POST.get('statesls', ''):
            judgerrors.append(u'行情程序需要重启吗？总不能让我随机吧！')

        if judgerrors:
            for error in judgerrors:
                errors.append(error.encode('utf8'))
        elif not judgerrors:
            getdclist = request.POST.getlist('datacenter')
            getexchlist = request.POST.getlist('stockexchange')
            getstatesls = request.POST.get('statesls')
            module_lock = moduleLock('state.sls', user)

            if getdclist:
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

            if '*' in getdclist:
                hostsum = len(result_host_set)
                sumset = set(result_host_set)
                jid = sapi.async_deploy_all(getstatesls)
            else:
                hostsum = len(result_host_set)
                sumset = set(result_host_set)
                tgt_list_to_str = ','.join(list(result_host_set))
                jid = sapi.async_deploy(tgt_list_to_str,getstatesls)

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

            log.info('Enter function findJob')
            find_job = findJob(result_host_set,jid)
            log.info('Quit function findJob')

            # db = db_operate()
            # time.sleep(30)
            # sql = 'select id,`return` from salt_returns where jid=%s'
            # result = db.select_table(settings.RETURNS_MYSQL,sql,str(jid))
            result = mysqlReturns(jid)


            hostrsum = len(result)
            returnset = set(result.keys())

            ret, hostfa, hosttr = outFormat(result)

            diffset = sumset.difference(returnset)
            for eachID in diffset:
                hostlist_data = HostList.objects.get(minionid=eachID)
                minion_ip = hostlist_data.ip
                diff_ip_list.append(minion_ip)
            hostunre = len(diffset)
            hostunrestr = ','.join(diff_ip_list)

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

    return render_to_response(
        'data_replace_history.html',
        {'ret': ret,
         'errors': errors,
         'hostsft': hostsft,
         'dc_list': dc_list,
         'data_centers': data_centers,
         'stock_exchanges': stock_exchanges
         },
        context_instance=RequestContext(request)
    )

# @login_required
# def dataReplaceAll(request):
#     '''
#
#     :param request:
#     :return:
#     '''
#
#     user = request.user
#     pattern_coarse = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#     pattern = re.compile(
#         r'(\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)')
#
#     arg_tardata = 'dzh_sls.mobileserver.data_compress'
#     arg_gettar = '/home/MobileServer/data.tar.gz'
#     arg_dist = 'dzh_sls.mobileserver.data_all'
#     var_cache_path = '/var/cache/salt/master/minions/'
#     source_path = '/srv/salt/dzh_store/mobileserver/tar/data.tar.gz'
#     dc_list = []
#     data_centers = {}
#     ts_list_new = []
#     stkindex_dict = {}
#
#     ret = {}
#     valcon = {}
#     hostsft = {}
#     jid = []
#     judgerrors = []
#     errors = []
#     #hostsum = 0
#     hostrsum = 0
#
#     result_dc = DataCenter.objects.all()
#     for dc in result_dc:
#         dc_list.append(dc.dcen)
#         data_centers[dc.dcen] = dc.dccn
#     dc_list.sort()
#
#     result_stkindex = StockIndex.objects.all()
#     for row_index in result_stkindex:
#         stkindex_dict[row_index.stkindex] = row_index.exchange
#
#     if request.method == 'POST':
#         form = RedataAllForms(request.POST)
#         if form.is_valid():
#             form_data_dict = form.cleaned_data
#             ds = form_data_dict['data_source']
#             dp = form_data_dict['data_path']
#             ts = form_data_dict['target_server']
#
#             try:
#                 ds_hostname = HostList.objects.get(ip=ds)
#                 ds_hn = ds_hostname.hostname
#             except:
#                 judgerrors.append(u'数据源服务器： %s 不在主机列表中！' % ds)
#
#             if ts:
#                 ts_list = ts.split(',')
#                 for ts_i in ts_list:
#                     if '*' not in ts_i.split():
#                         match_coarse = pattern_coarse.search(ts_i)
#                         if match_coarse:
#                             match = pattern.search(ts_i)
#                             if match:
#                                 try:
#                                     result_ts = HostList.objects.get(ip=match.group())
#                                     ts_list_new.append(result_ts.hostname)
#                                 except DoesNotExist:
#                                     judgerrors.append(u'目标主机 %s 不在主机列表中！' % ts_i)
#                             else:
#                                 judgerrors.append(u'目标主机地址 %s 不合法!' % ts_i )
#                         else:
#                             try:
#                                 result_ts = HostList.objects.get(hostname=ts_i)
#                                 ts_list_new.append(ts_i)
#                             except DoesNotExist:
#                                 judgerrors.append(u'目标主机 %s 不在主机列表中！' % ts_i)
#                     else:
#                         ts_list_new.append(ts_i)
#             if not request.POST.get('datacenter', '') and not ts_list_new:
#                 judgerrors.append(u'需要指定目标机房或目标机房，才能允许后续操作！')
#             else:
#                 get_dc_list = request.POST.getlist('datacenter')
#
#
#             if not judgerrors:
#                 if ts:
#                     tgt_set = manageTgt(ts)
#                 else:
#                     tgt_set = set([])
#
#                 if get_dc_list:
#                     if '*' in get_dc_list:
#                         result_host_set = set(['*'])
#                     else:
#                         result_host_set = hostSet(get_dc_list)
#                 else:
#                     result_host_set = set([])
#
#                 tgt_list = list(tgt_set.union(result_host_set))
#                 tgt_judge, tgtminis = judgeTarget(tgt_list)
#                 if not tgt_judge:
#                     judgerrors.append(u'目标主机只能形如zhaogb-201、zhaogb-*、* 这三种(可多个用英文逗号隔开)！')
#                 else:
#                     sapi = SaltAPI(
#                         url=settings.SALT_API['url'],
#                         username=settings.SALT_API['user'],
#                         password=settings.SALT_API['password'])
#                     tar_data_fun = 'state.sls'
#                     tar_data = sapi.masterToMinion(ds_hn,tar_data_fun,arg_tardata)
#                     if tar_data:
#                         tk = tar_data['return'][0][ds_hn].keys()
#                         result_tar_data = tar_data['return'][0][ds_hn][tk[0]]['result']
#                         if result_tar_data:
#                             get_tar_data_fun = 'cp.push'
#                             get_tar_data = sapi.masterToMinion(ds_hn,get_tar_data_fun,arg_gettar)
#                             if get_tar_data:
#                                 get_tar_status = get_tar_data['return'][0][ds_hn]
#                                 if get_tar_status:
#                                     data_path = os.path.join(var_cache_path, ds_hn, 'files', arg_gettar[1:])
#                                     if os.path.exists(data_path):
#                                         os.rename(data_path, source_path)
#                                         if os.path.exists(source_path):
#                                             if '*' in tgt_list:
#                                                 hostsum = len(result_host_set)
#                                                 sumset = set(result_host_set)
#                                                 obj = sapi.async_deploy_all(arg_dist)
#                                             else:
#                                                 hostsum = len(result_host_set)
#                                                 sumset = set(result_host_set)
#                                                 tgt_list_to_str = ','.join(result_host_set)
#                                                 obj = sapi.async_deploy(tgt_list_to_str,arg_dist)
#                                             jid.append(obj)
#
#                                             if get_dc_list:
#                                                 operate_tgt = get_dc_list[0]
#                                             else:
#                                                 operate_tgt = 'unknown'
#
#                                             op_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
#                                             op_user = arg_dist
#                                             op_tgt = '%s...' % operate_tgt
#                                             p1 = OperateRecord.objects.create(
#                                                 nowtime=op_time,
#                                                 username=user,
#                                                 user_operate=op_user,
#                                                 simple_tgt=op_tgt,
#                                                 jid=jid[0])
#
#                                             db = db_operate()
#                                             for i in jid:
#                                                 time.sleep(30)
#                                                 sql = 'select id,`return` from salt_returns where jid=%s'
#                                                 result = db.select_table(settings.RETURNS_MYSQL,sql,str(i))
#                                                 hostrsum = len(result)
#                                                 returnset = set(result.keys())
#
#                                             ret, hostfa, hosttr = outFormat(result)
#
#                                             diffset = sumset.difference(returnset)
#                                             hostunre = len(diffset)
#                                             hostunrestr = ','.join(list(diffset))
#
#                                             hostsft['sum'] = hostsum
#                                             hostsft['rsum'] = hostrsum
#                                             hostsft['unre'] = hostunre
#                                             hostsft['unrestr'] = hostunrestr
#                                             hostsft['fa'] = hostfa
#                                             hostsft['tr'] = hosttr
#
#                                             os.remove(source_path)
#
#                                             saveRecord = ReturnRecord.objects.create(
#                                                 jid=jid[0],
#                                                 tgt_total=hostsum,
#                                                 tgt_ret=hostrsum,
#                                                 tgt_succ=hosttr,
#                                                 tgt_fail=hostfa,
#                                                 tgt_unret=hostunre,
#                                                 tgt_unret_list=hostunrestr
#                                             )
#
#                                     else:
#                                         judgerrors.append(u'Master cache目录下无data.tar.gz数据包！')
#                                 else:
#                                     judgerrors.append(u'拉取数据失败（拉取数据操作返回结果为False）！')
#                             else:
#                                 judgerrors.append(u'拉取数据命令执行失败(Salt-api返回结果为空)！')
#                         else:
#                             judgerrors.append(u'打包数据失败（打包数据操作返回结果为False）！')
#                     else:
#                         judgerrors.append(u'打包数据命令执行失败(Salt-api返回结果为空)！')
#     else:
#         form = RedataAllForms(initial={'data_path': '/home/MobileServer/DATA/'})
#
#     if judgerrors:
#         for error in judgerrors:
#             errors.append(error.encode('utf8'))
#
#     return render_to_response(
#         'data_replace_all.html',
#         {'form': form,
#          'dc_list': dc_list,
#          'data_centers': data_centers,
#          'ret': ret,
#          'errors': errors,
#          'hostsft': hostsft,
#          'stkindex_dict': stkindex_dict
#          },
#         context_instance=RequestContext(request)
#     )
