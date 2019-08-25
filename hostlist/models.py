# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
class DzhUser(models.Model):
    username = models.CharField(max_length=30, blank=True, verbose_name=u'用户名')
    engineer = models.CharField(max_length=30, blank=True, verbose_name=u'维护人员')

    def __unicode__(self):
        return u'%s %s' % (self.username, self.engineer)


class DataCenter(models.Model):
    dc_en = models.CharField(max_length=30, blank=True, verbose_name=u'机房简称')
    dc_cn = models.CharField(max_length=30, blank=True, verbose_name=u'机房全称')

    def __unicode__(self):
        return u'%s %s' % (self.dc_en, self.dc_cn)


class NetworkOperator(models.Model):
    no_en = models.CharField(max_length=30, blank=True, verbose_name=u'运营商简称')
    no_cn = models.CharField(max_length=30, blank=True, verbose_name=u'运营商全称')

    def __unicode__(self):
        return u'%s %s' % (self.no_en, self.no_cn)


class ProvinceArea(models.Model):
    pa_en = models.CharField(max_length=30, blank=True, verbose_name=u'省份地区简称')
    pa_cn = models.CharField(max_length=30, blank=True, verbose_name=u'省份地区全称')

    def __unicode__(self):
        return u'%s %s' % (self.pa_en, self.pa_cn)


class Category(models.Model):
    category_en = models.CharField(max_length=30, blank=True, verbose_name=u'类别简称')
    category_cn = models.CharField(max_length=30, blank=True, verbose_name=u'类别全称')

    def __unicode__(self):
        return u'%s %s' % (self.category_en, self.category_cn)


class HostList(models.Model):
    ip = models.CharField(max_length=15, blank=True, verbose_name=u'IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    minion_id = models.CharField(max_length=60, verbose_name=u'MinionID')
    no_cn = models.CharField(max_length=30, verbose_name=u'运营商全称')
    category_cn = models.CharField(max_length=30, blank=True, verbose_name=u'类别')
    pa_cn = models.CharField(max_length=30, verbose_name=u'地区全称')
    dc_cn = models.CharField(max_length=30, blank=True, verbose_name=u'机房全称')
    engineer = models.CharField(max_length=30, blank=True, verbose_name=u'维护人员')
    mac_addr = models.CharField(max_length=20, blank=True, verbose_name=u'MAC地址')
    main_source_ip = models.CharField(max_length=30, blank=True, verbose_name=u'主行情源')
    backup_source_ip = models.CharField(max_length=30, blank=True, verbose_name=u'备行情源')
    # dccn = models.ForeignKey(dataCenter, related_name='datacenter_hostlist')
    lic_date = models.CharField(max_length=30, blank=True, verbose_name=u'授权日期')
    lic_status = models.CharField(max_length=30, blank=True, verbose_name=u'授权状态')
    # engineer = models.ForeignKey(dzhuser, related_name='dzhuser_hostlist')
    id_ip = models.CharField(max_length=15, blank=True, verbose_name=u'MinionID中的IP地址')
    ip_same = models.CharField(max_length=10, blank=True, verbose_name=u'IP地址一致性')
    remark = models.TextField(max_length=200, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.hostname, self.ip, self.category_cn, self.dc_cn, self.engineer)

    class Meta:
        ordering = ['minionid']
