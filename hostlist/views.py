# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from hostlist.form import *
from hostlist.models import Dzhuser, DataCenter, HostList
from dzhops.mysql import db_operate
from dzhops import settings

@login_required
def host_list_manage(request,id=None):
    """
    Manage Host List
    """
    #user = request.user
    if id:
        host_list = get_object_or_404(HostList, pk=id)
        action = 'edit'
        page_name = '编辑主机'
        db = db_operate() 
        sql = 'select ip from hostlist_hostlist where id = %s' % (id)
        ret = db.mysql_command(settings.DATABASES,sql)
    else:
        host_list = HostList()
        action = 'add'   
        page_name = '新增主机'

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        if delete:
           host_list = get_object_or_404(HostList, pk=id)
           host_list.delete()
           return HttpResponseRedirect(reverse('host_list'))

    if request.method == 'POST': 
        form = HostsListForm(request.POST,instance=host_list)
        operate = request.POST.get('operate')
        if form.is_valid():
            if action == 'add':
                form.save()
                return HttpResponseRedirect(reverse('host_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    return HttpResponseRedirect(reverse('host_list'))
                else:
                    pass
    else:
        form = HostsListForm(instance=host_list)

    return render_to_response('host_manage.html',
           {"form": form,
            "page_name": page_name,
            "action": action,
           },context_instance=RequestContext(request))

@login_required
def host_list(request):
    """
    Show hosts for data center or engineer
    """
    user = request.user

    dcs_list = []
    #eng_list = []

    all_datacenters = DataCenter.objects.all()
    for dc in all_datacenters:
        dcs_list.append(dc.dccn)
    #all_engineers = Dzhuser.objects.all()
    #for eng in all_engineers:
    #    eng_list.append(eng.engineer)

    dcs_list.sort()
    #eng_list.sort()

    return render_to_response(
        'host_list.html',
        {'all_dcs_list': dcs_list},
        context_instance=RequestContext(request)
    )

@login_required
def engineerList(request):
    """
    Show hosts for engineer
    """
    user = request.user

    eng_list = []

    all_engineers = Dzhuser.objects.all()
    for eng in all_engineers:
        eng_list.append(eng.engineer)

    eng_list.sort()

    return render_to_response(
        'host_list_engineer.html',
        {'all_eng_list': eng_list},
        context_instance=RequestContext(request)
    )


@login_required
def showList(request):
    '''
    show datacenter list or engineer list;
    :param request: datacenter='测试机房1' or engineer = '赵贵斌';
    :return: mysql select * from host_list where datacenter='测试机房1' or engineer = '赵贵斌';
    '''
    if 'datacenter' in request.GET:
        dc = request.GET.get('datacenter')
        result = HostList.objects.filter(dccn=dc).order_by('engineer', 'ip')
    elif 'engineer' in request.GET:
        eng = request.GET.get('engineer')
        result = HostList.objects.filter(engineer=eng).order_by('dccn', 'ip')
    else:
        pass

    return render_to_response(
        'show_list.html',
        {'db_result': result},
        context_instance=RequestContext(request)
    )

