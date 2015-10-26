# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class HostList(models.Model):
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    ip = models.CharField(max_length=15,  blank=True,verbose_name=u'IP地址')
    macaddr = models.CharField(max_length=20,  blank=True,verbose_name=u'MAC地址')
    zsourceip = models.CharField(max_length=30,  blank=True,verbose_name=u'主行情源')
    bsourceip = models.CharField(max_length=30,  blank=True,verbose_name=u'备行情源')
    licdate = models.CharField(max_length=30,  blank=True,verbose_name=u'授权日期')
    licstatus = models.CharField(max_length=30, blank=True, verbose_name=u'授权状态')
    engineer = models.CharField(max_length=30, blank=True, verbose_name=u'维护人员')
    remark = models.TextField(max_length=200, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s - %s - %s' %(self.hostname, self.ip, self.macaddr, self.remark)
