# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render_to_response('index.html')

def login(request):
    ret = {'zhaogb-201':'zhaogb-201','zhaogb-202':'zhaogb-202'}
    #ret = {'zhaogb-201':{'cont':'zhaogb-201','status': 'True'},'zhaogb-202':{'cont':'zhaogb-202','status': 'Fasle'},'zhaogb-203':{'cont':'zhaogb-203','status': 'Fasle'},'zhaogb-205':{'cont':'zhaogb-205','status': 'True'}}
    #ret = {u'file_|-info_so_1_|-/usr/lib64/libodbc.so.1_|-managed': {u'comment': u'File /usr/lib64/libodbc.so.1 is in the correct state', u'name': u'/usr/lib64/libodbc.so.1', u'start_time': u'09:33:32.468444', u'result': True, u'duration': 17.170000000000002, u'__run_num__': 2, u'changes': {}}, u'cmd_|-info_install_|-tar zxf /tmp/info.tar.gz -C /home/_|-run': {u'comment': u'Command "tar zxf /tmp/info.tar.gz -C /home/" run', u'name': u'tar zxf /tmp/info.tar.gz -C /home/', u'start_time': u'09:33:32.278982', u'result': True, u'duration': 188.48699999999999, u'__run_num__': 1, u'changes': {u'pid': 10564, u'retcode': 0, u'stderr': u'', u'stdout': u''}}, u'file_|-info_so_3_|-/usr/lib64/libltdl.so.3_|-managed': {u'comment': u'File /usr/lib64/libltdl.so.3 is in the correct state', u'name': u'/usr/lib64/libltdl.so.3', u'start_time': u'09:33:32.499477', u'result': True, u'duration': 6.6440000000000001, u'__run_num__': 4, u'changes': {}}, u'file_|-info_install_|-/tmp/info.tar.gz_|-managed': {u'comment': u'File /tmp/info.tar.gz is in the correct state', u'name': u'/tmp/info.tar.gz', u'start_time': u'09:33:31.743953', u'result': True, u'duration': 533.60500000000002, u'__run_num__': 0, u'changes': {}}, u'file_|-info_so_2_|-/usr/lib64/libodbc.so.2_|-managed': {u'comment': u'File /usr/lib64/libodbc.so.2 is in the correct state', u'name': u'/usr/lib64/libodbc.so.2', u'start_time': u'09:33:32.485824', u'result': True, u'duration': 13.279, u'__run_num__': 3, u'changes': {}}, u'file_|-info_service_|-/etc/init.d/infoservd_|-managed': {u'comment': u'File /etc/init.d/infoservd is in the correct state', u'name': u'/etc/init.d/infoservd', u'start_time': u'09:33:32.506618', u'result': True, u'duration': 8.1760000000000002, u'__run_num__': 5, u'changes': {}}}
    return render_to_response('login.html',{'ret': ret})
