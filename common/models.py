# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class OperateRecord(models.Model):
    nowtime = models.DateTimeField(blank=True, null=True, verbose_name=u'操作时间')
    username = models.CharField(max_length=20, blank=True, verbose_name=u'用户名')
    user_operate = models.CharField(max_length=100, blank=True, verbose_name=u'用户操作')
    simple_tgt = models.CharField(max_length=30, blank=True, verbose_name=u'目标简述')
    jid = models.CharField(max_length=255, blank=True, verbose_name=u'jid')

    def __unicode__(self):
        return u'%s %s %s %s %s' %(self.nowtime, self.username, self.user_operate, self.simple_tgt, self.jid)

class ReturnRecord(models.Model):
    '''
    salt result record
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

class DeployModules(models.Model):
    '''
    state sls for deploy modules;
    '''
    slsfile = models.CharField(max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)

class ConfigUpdate(models.Model):
    '''
    state sls for deploy modules;
    '''
    slsfile = models.CharField(max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)

class CommonOperate(models.Model):
    '''
    state sls for deploy modules;
    '''
    slsfile = models.CharField(max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)

class ModulesLock(models.Model):
    '''

    '''
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')
    status = models.CharField(max_length=30, blank=True, verbose_name=u'使用状态')
    user = models.CharField(max_length=30, blank=True, verbose_name=u'用户')

    def __unicode__(self):
        return u'%s %s %s' % (self.module, self.status, self.user)

class Jids(models.Model):
    jid = models.CharField(primary_key=True, max_length=255)
    load = models.TextField()
    class Meta:
        managed = False
        db_table = 'jids'
    def __unicode__(self):
        return u'%s %s' % (self.jid, self.load)

class SaltReturns(models.Model):
    useless = models.AutoField(primary_key=True)
    fun = models.CharField(max_length=50)
    jid = models.CharField(max_length=255)
    return_field = models.TextField(db_column='return') # Field renamed because it was a Python reserved word.
    id = models.CharField(max_length=255)
    success = models.CharField(max_length=10)
    full_ret = models.TextField()
    alter_time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'salt_returns'
    def __unicode__(self):
        return u'%s %s %s' % (self.jid, self.id, self.return_field)