# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from record.models import OperateRecord, ReturnRecord
from saltstack.util import mysqlReturns, outFormat
# Create your views here.

@login_required
def record(request):
    user = request.user.username
    page_size = 10

    all_record = OperateRecord.objects.order_by('-id')
    paginator = Paginator(all_record, page_size)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    # page_id = range(((page-1)*13+1),(page*13+1))

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'record_list.html',
        {'posts': posts,
         # 'page_id': page_id,
         }
    )


@login_required
def recordDetail(request):
    user = request.user.username
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

        # db = db_operate()
        # sql = 'select id,`return` from salt_returns where jid=%s'
        # jid_result = db.select_table(settings.RETURNS_MYSQL, sql, str(job_id))
        jid_result = mysqlReturns(job_id)
        ret, hostfa, hosttr = outFormat(jid_result)

    else:
        jid_record = ''
        ret = {}

    return render(
        request,
        'record_detail.html',
        {'jid_record': jid_record,
         'hostsft': hostsft,
         'ret': ret
         }
    )
