# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from hostlist.models import Dzhuser, DataCenter, HostList

import json, logging


log = logging.getLogger('dzhops')

@login_required
def assetList(request):
    '''
    展示所有服务器信息；
    :param request:
    :return:
    '''
    user = request.user.username
    dc_dict = {}
    engi_dict = {}
    serv_dict = {}
    serv_list = []
    ip_list = []

    dc = DataCenter.objects.all()
    for i in dc:
        dc_dict[i.dcen] = i.dccn
    eg = Dzhuser.objects.all()
    for j in eg:
        engi_dict[j.username] = j.engineer
    db_result = HostList.objects.all()
    for db in db_result:
        ip_list.append(db.ip)
        serv_dict[db.ip] = [db.ip, db.hostname, db.minionid, db.nocn, db.catagorycn, db.pacn, db.dccn, db.engineer]
    ip_list.sort()
    for ip in ip_list:
        info = serv_dict.get(ip)
        serv_list.append(info)

    return render(
        request,
        'asset_list.html',
        {
            'dc_dict': dc_dict,
            'engi_dict': engi_dict,
            'serv_list': serv_list
        }
    )

@login_required
def assetListAPI(request):
    '''
    当前端选择机房与维护人员的时候，通过该接口提交请求并返回数据；
    :param request:
    :return:
    '''
    user = request.user.username
    ip_list = []
    serv_list = []
    serv_dict = {}

    if request.method == 'GET':
        dc = request.GET.get('dcen', '')
        eg = request.GET.get('engi', '')

        if dc == 'All_DC' and eg == 'ALL_ENGI':
            result = HostList.objects.all()
        elif dc == 'All_DC' and eg != 'ALL_ENGI':
            eg_result = Dzhuser.objects.get(username=eg)
            result = HostList.objects.filter(engineer=eg_result.engineer)
        elif dc != 'All_DC' and eg == 'ALL_ENGI':
            dc_result = DataCenter.objects.get(dcen=dc)
            result = HostList.objects.filter(dccn=dc_result.dccn)
        elif dc != 'All_DC' and eg != 'ALL_ENGI':
            eg_result = Dzhuser.objects.get(username=eg)
            dc_result = DataCenter.objects.get(dcen=dc)
            result = HostList.objects.filter(dccn=dc_result.dccn, engineer=eg_result.engineer)
        else:
            log.error('Unexpected execution here.')

        for data in result:
            ip_list.append(data.ip)
            serv_dict[data.ip] = [
                data.ip,
                data.hostname,
                data.minionid,
                data.nocn,
                data.catagorycn,
                data.pacn,
                data.dccn,
                data.engineer
            ]
        ip_list.sort()
        for ip in ip_list:
            info = serv_dict.get(ip)
            serv_list.append(info)
    serv_info_json = json.dumps(serv_list)

    return HttpResponse(serv_info_json, content_type="application/json")

