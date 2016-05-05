# -*- coding: utf-8 -*-
from hostlist.models import HostList, Dzhuser
import logging

log = logging.getLogger('dzhops')

def clearUpMinionKyes(idlist, dc, eg):
    '''
    对Minion id进行整理，返回对应状态、机房、维护人员的minion id;
    :param idlist: acp/pre/rej（分别表示已经接受、未接受、已拒绝三个状态）
    :param dc: 机房英文简称
    :param eg: 维护人员用户名，英文简称；
    :return: 过滤后的minion id 组成的列表；
    '''
    if dc == 'DC_ALL' and eg == 'EG_ALL':
        result = idlist
    elif dc != 'DC_ALL' and eg == 'EG_ALL':
        result = []
        for id in idlist:
            id_dcen = id.split("_")
            if id_dcen[3] == dc:
                result.append(id)
    elif dc == 'DC_ALL' and eg != 'EG_ALL':
        eg_id_list = []
        engi_result = Dzhuser.objects.get(username=eg)
        data = HostList.objects.filter(engineer=engi_result.engineer)
        for row in data:
            eg_id_list.append(row.minionid)
        result = list(set(idlist).intersection(set(eg_id_list)))
    elif dc != 'DC_ALL' and eg != 'EG_ALL':
        dc_id_list = []
        eg_id_list = []
        for id in idlist:
            id_dcen = id.split("_")
            if id_dcen[3] == dc:
                dc_id_list.append(id)
        engi_result = Dzhuser.objects.get(username=eg)
        data = HostList.objects.filter(engineer=engi_result.engineer)
        for row in data:
            eg_id_list.append(row.minionid)
        result = list(set(dc_id_list).intersection(set(eg_id_list)))
    else:
        result = []
        log.error("Unexpected execution here.")

    return result