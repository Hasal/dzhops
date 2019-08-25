# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from hostlist.models import DzhUser, DataCenter, HostList

import logging

log = logging.getLogger('dzhops')


@login_required
def asset_list(request):
    """
    展示所有服务器信息；
    :param request: 
    :return: 
    """
    # user = request.user.username
    dc_dict = {}
    engi_dict = {}

    dc = DataCenter.objects.all()
    for i in dc:
        dc_dict[i.dcen] = i.dccn
    eg = DzhUser.objects.all()
    for j in eg:
        engi_dict[j.username] = j.engineer
    db_result = HostList.objects.all()
    srv_list = filter_data(db_result)

    return render(
        request,
        'asset_list.html',
        {
            'dc_dict': dc_dict,
            'engi_dict': engi_dict,
            'serv_list': srv_list
        }
    )


@login_required
@require_GET
def asset_list_api(request):
    """
    当前端选择机房与维护人员的时候，通过该接口提交请求并返回数据；
    :param request:
    :return:
    """
    user = request.user.username

    dc = request.GET.get('dcen', '')
    eg = request.GET.get('engi', '')
    result = []
    if dc == 'All_DC' and eg == 'ALL_ENGI':
        result = HostList.objects.all()
    elif dc == 'All_DC' and eg != 'ALL_ENGI':
        eg_result = DzhUser.objects.get(username=eg)
        result = HostList.objects.filter(engineer=eg_result.engineer)
    elif dc != 'All_DC' and eg == 'ALL_ENGI':
        dc_result = DataCenter.objects.get(dcen=dc)
        result = HostList.objects.filter(dccn=dc_result.dccn)
    elif dc != 'All_DC' and eg != 'ALL_ENGI':
        eg_result = DzhUser.objects.get(username=eg)
        dc_result = DataCenter.objects.get(dcen=dc)
        result = HostList.objects.filter(dccn=dc_result.dccn, engineer=eg_result.engineer)
    else:
        log.error('Unexpected execution here.')

    srv_list = filter_data(result)
    return JsonResponse(srv_list)


def filter_data(models_data):
    ip_list = []
    srv_list = []
    srv_dict = {}

    for i in models_data:
        ip_list.append(i.ip)
        srv_dict[i.ip] = [
            i.ip,
            i.hostname,
            i.minionid,
            i.nocn,
            i.catagorycn,
            i.pacn,
            i.dccn,
            i.engineer
        ]
    ip_list.sort()
    for ip in ip_list:
        srv_list.append(srv_dict.get(ip))
    return srv_list
