# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from dzhops import settings
from index.models import MiniKeys, ProcStatus, ServStatus
from index.forms import ChangePasswordForms, UploadFileForm
from record.models import OperateRecord
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
    return render(
        request,
        'index_upload.html',
        {'form': form}
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
    return render(
        request,
        'profile.html',
        {
            'form': form,
            'tips': tips
        }
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
        operate_rec = OperateRecord.objects.order_by('-id')[0:8]
        for result in operate_rec:
            streslut += '%s %s %s %s\n' % (result.nowtime, result.username, result.user_operate, result.simple_tgt)
    except Exception, e:
        log.error("No data acquired.")

    return render(
        request,
        'index.html',
        {
            'ret': ret,
            'stret': streslut
        }
    )
