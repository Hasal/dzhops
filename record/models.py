# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class OperateRecord(models.Model):
    '''
    记录用户操作信息；
    '''
    nowtime = models.DateTimeField(blank=True, null=True, verbose_name=u'操作时间')
    username = models.CharField(max_length=20, blank=True, verbose_name=u'用户名')
    user_operate = models.CharField(max_length=100, blank=True, verbose_name=u'用户操作')
    simple_tgt = models.CharField(max_length=30, blank=True, verbose_name=u'目标简述')
    jid = models.CharField(max_length=255, blank=True, verbose_name=u'jid')

    def __unicode__(self):
        return u'%s %s %s %s %s' %(self.nowtime, self.username, self.user_operate, self.simple_tgt, self.jid)

class ReturnRecord(models.Model):
    '''
    记录用户操作返回结果信息；
    '''

    jid = models.CharField(max_length=255, blank=True, verbose_name=u'jid')
    tgt_total = models.CharField(max_length=10, blank=True, verbose_name=u'目标总数')
    tgt_ret = models.CharField(max_length=10, blank=True, verbose_name=u'有返回结果的主机数量')
    tgt_succ = models.CharField(max_length=10, blank=True, verbose_name=u'成功的主机数量')
    tgt_fail = models.CharField(max_length=10, blank=True, verbose_name=u'失败的主机数量')
    tgt_unret = models.CharField(max_length=10, blank=True, verbose_name=u'未返回结果的主机数量')
    tgt_unret_list = models.TextField(blank=True, verbose_name=u'未返回结果的主机列表')

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.jid, self.tgt_total, self.tgt_ret, self.tgt_succ, self.tgt_fail, self.tgt_unret)