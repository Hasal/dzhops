# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.template.context import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from dzhops import settings
from index.models import MiniKeys, ProcStatus, ServStatus
from index.forms import ChangePasswordForms, UploadFileForm
from common.models import OperateRecord
# import system libs
import Image
import os
import shutil
import logging

log = logging.getLogger('dzhops')


def imageResize(img, username):
    '''
    Image resize to 58 * 58;
    :param img:
    :return:
    '''
    try:
        standard_size = (58, 58)
        file_type = '.jpg'
        user_pic_list = [username, file_type]
        log.debug(str(user_pic_list))
        user_pic_str = ''.join(user_pic_list)
        log.debug('37')
        log.debug('user_pic_path: %s' % str(settings.STATICFILES_DIRS))
        user_pic_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', user_pic_str)
        im = Image.open(img)
        im_new = im.resize(standard_size, Image.ANTIALIAS)
        im_new.save(user_pic_path, 'JPEG', quality=100)
        log.info('The user pic resize successed')
        try:
            all_static = settings.STATIC_ROOT
            all_static_url = os.path.join(all_static, 'img')
        except AttributeError, e:
            all_static_url = ''
            log.info('The config settings.py no STATIC_ROOT attribute')
        if all_static_url and os.path.exists(all_static_url):
            shutil.copy(user_pic_path, all_static_url)
            log.info('The user picture copy to all_static_url')
        else:
            log.debug('The all_static_url is None or do not exist')
    except Exception, e:
        log.error(str(e))


def handle_uploaded_file(f, filename):
    picname = '%s.jpg' % filename
    filepath = os.path.join(settings.STATICFILES_DIRS[0], 'img', picname)
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    log.debug('user pic upload and save')
    imageResize(filepath, filename)
    log.debug('The user picture resize and save')


@login_required
def upload_file(request):
    user = request.user.username
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user)
            return HttpResponseRedirect('/accounts/upload/')
    else:
        form = UploadFileForm()
    return render_to_response(
        'index_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )


@login_required
def profile(request):
    '''
    :param request:
    :return:
    '''
    user = request.user.username
    tips = ''
    if request.method == 'POST':
        form = ChangePasswordForms(request.POST)
        if form.is_valid():
            form_data_dict = form.cleaned_data
            passwd_old = form_data_dict['password_old']
            passwd_new = form_data_dict['password_new']
            passwd_new_again = form_data_dict['password_new_again']

            user_auth = authenticate(username=user, password=passwd_old)
            if user_auth is not None:
                user_pwd = User.objects.get(username=user)
                user_pwd.set_password(passwd_new)
                user_pwd.save()
                tips = u'密码修改成功！'
            else:
                tips = u'原密码不正确，请重新输入！'
    else:
        form = ChangePasswordForms()

    tips = tips.encode('utf-8')
    return render_to_response(
        'profile.html',
        {
            'form': form,
            'tips': tips
        },
        context_instance=RequestContext(request),
    )


@login_required
def index(request):
    '''
    index page
    '''

    ret = {}

    try:
        server_status = ServStatus.objects.order_by('-id')[0]
        # SELECT * from `servstatus` order by id DESC limit 1

        ret['nowtime'] = server_status.nowtime
        ret['sysone'] = server_status.sysone
        ret['sysfive'] = server_status.sysfive
        ret['sysfifteen'] = server_status.sysfifteen
        ret['cpuperc'] = server_status.cpuperc
        ret['memtotal'] = server_status.memtotal
        ret['memused'] = server_status.memused
        ret['memperc'] = server_status.memperc
        ret['disktotal'] = server_status.disktotal
        ret['diskused'] = server_status.diskused
        ret['diskperc'] = server_status.diskperc

    # except OperationalError,e:
    except Exception, e:
        # ret['serv_error_code'] = e[0]
        # ret['serv_error_content'] = e[1]
        ret['nowtime'] = 'Null'
        ret['sysone'] = 'Null'
        ret['sysfive'] = 'Null'
        ret['sysfifteen'] = 'Null'
        ret['cpuperc'] = 'Null'
        ret['memtotal'] = 'Null'
        ret['memused'] = 'Null'
        ret['memperc'] = 'Null'
        ret['disktotal'] = 'Null'
        ret['diskused'] = 'Null'
        ret['diskperc'] = 'Null'

    try:
        proc_status = ProcStatus.objects.order_by('-id')[0]
        # SELECT * from `procstatus` order by id DESC limit 1

        ret['proctime'] = proc_status.nowtime

        if proc_status.saltproc == 0:
            ret['saltst'] = '正常'
        elif proc_status.saltproc == 1:
            ret['saltst'] = '异常'
        else:
            ret['saltst'] = 'UNKNOWN'

        if proc_status.apiproc == 0:
            ret['apist'] = '正常'
        elif proc_status.apiproc == 1:
            ret['apist'] = '异常'
        else:
            ret['apist'] = 'UNKNOWN'

        if proc_status.myproc == 0:
            ret['myst'] = '正常'
        elif proc_status.myproc == 1:
            ret['myst'] = '异常'
        else:
            ret['myst'] = 'UNKNOWN'

        if proc_status.snmproc == 0:
            ret['snmpst'] = '正常'
        elif proc_status.snmproc == 1:
            ret['snmpst'] = '异常'
        else:
            ret['snmpst'] = 'UNKNOWN'

    # except OperationalError,e:
    except Exception, e:
        # ret['proc_error_code'] = e[0]
        # ret['proc_error_content'] = e[1]
        ret['saltst'] = 'Null'
        ret['apist'] = 'Null'
        ret['myst'] = 'Null'
        ret['snmpst'] = 'Null'

    try:
        minion_keys = MiniKeys.objects.order_by('-id')[0]
        # SELECT * from `minikeys` order by id DESC limit 1

        ret['mktime'] = minion_keys.nowtime
        ret['num_miniall'] = minion_keys.miniall
        ret['num_miniup'] = minion_keys.minion
        ret['num_minidown'] = minion_keys.miniout
        ret['num_mini'] = minion_keys.keyall
        ret['num_minipre'] = minion_keys.keypre
        ret['num_minirej'] = minion_keys.keyrej

    # except OperationalError,e:
    except Exception, e:
        # ret['mini_error_code'] = e[0]
        # ret['mini_error_content'] = e[1]
        ret['mktime'] = 'Null'
        ret['num_miniall'] = 'Null'
        ret['num_miniup'] = 'Null'
        ret['num_minidown'] = 'Null'
        ret['num_mini'] = 'Null'
        ret['num_minipre'] = 'Null'
        ret['num_minirej'] = 'Null'

    streslut = ''
    try:
        operate_rec = OperateRecord.objects.order_by('-id')[0:5]
        for result in operate_rec:
            streslut += '%s %s %s %s\n' % (result.nowtime, result.username, result.user_operate, result.simple_tgt)
            # operate_rec_0 = OperateRecord.objects.order_by('-id')[0]
            # operate_rec_1 = OperateRecord.objects.order_by('-id')[1]
            # operate_rec_2 = OperateRecord.objects.order_by('-id')[2]

            # ret['op_time_0'] = operate_rec_0.nowtime
            # ret['op_time_1'] = operate_rec_1.nowtime
            # ret['op_time_2'] = operate_rec_2.nowtime
            # ret['op_user_0'] = operate_rec_0.username
            # ret['op_user_1'] = operate_rec_1.username
            # ret['op_user_2'] = operate_rec_2.username
            # ret['op_user_op_0'] = operate_rec_0.result
            # ret['op_user_op_1'] = operate_rec_1.user_operate
            # ret['op_user_op_2'] = operate_rec_2.user_operate
            # ret['op_tgt_0'] = operate_rec_0.simple_tgt
            # ret['op_tgt_1'] = operate_rec_1.simple_tgt
            # ret['op_tgt_2'] = operate_rec_2.simple_tgt

    # except OperationalError,e:
    except Exception, e:
        # ret['op_error_code'] = e[0]
        # ret['op_error_content'] = e[1]
        ret['op_time_0'] = 'Null'
        ret['op_time_1'] = 'Null'
        ret['op_time_2'] = 'Null'
        ret['op_user_0'] = 'Null'
        ret['op_user_1'] = 'Null'
        ret['op_user_2'] = 'Null'
        ret['op_user_op_0'] = 'Null'
        ret['op_user_op_1'] = 'Null'
        ret['op_user_op_2'] = 'Null'
        ret['op_tgt_0'] = 'Null'
        ret['op_tgt_1'] = 'Null'
        ret['op_tgt_2'] = 'Null'

    return render_to_response('index.html', {'ret': ret, 'stret': streslut}, context_instance=RequestContext(request))
