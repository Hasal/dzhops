# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class DangerCommand(models.Model):
    '''
    将危险的命令存进该库，远程执行命令功能会来该表取数据进行对比；
    '''
    command = models.CharField(max_length=50, unique=True, verbose_name=u'命令')
    status = models.CharField(max_length=20, verbose_name=u'状态')

    def __unicode__(self):
        return u'{0} {1}'.format(self.command, self.status)


class ModulesLock(models.Model):
    '''
    模块是否有人正在使用相关信息保存在该表；
    '''
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')
    status = models.CharField(max_length=30, blank=True, verbose_name=u'使用状态')
    user = models.CharField(max_length=30, blank=True, verbose_name=u'用户')

    def __unicode__(self):
        return u'%s %s %s' % (self.module, self.status, self.user)


class DeployModules(models.Model):
    '''
    程序部署sls文件表;
    '''
    slsfile = models.CharField(
        max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)


class ConfigUpdate(models.Model):
    '''
    配置更新sls文件表;
    '''
    slsfile = models.CharField(
        max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)


class CommonOperate(models.Model):
    '''
    日常维护sls文件表;
    '''
    slsfile = models.CharField(
        max_length=255, blank=True, verbose_name=u'sls文件')
    module = models.CharField(max_length=30, blank=True, verbose_name=u'模块名称')

    def __unicode__(self):
        return u'%s %s' % (self.slsfile, self.module)


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
    # Field renamed because it was a Python reserved word.
    return_field = models.TextField(db_column='return')
    id = models.CharField(max_length=255)
    success = models.CharField(max_length=10)
    full_ret = models.TextField()
    alter_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'salt_returns'

    def __unicode__(self):
        return u'%s %s %s' % (self.jid, self.id, self.return_field)
