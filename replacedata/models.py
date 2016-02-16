# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class StockExchage(models.Model):
    '''
    All Stock Exchanges;
    '''

    stkexchen = models.CharField(max_length=6, blank = True, verbose_name = u'股票市场英文简称')
    stkexchcn = models.CharField(max_length=20, blank = True, verbose_name = u'股票市场中文名称')

    def __unicode__(self):
        return u'%s %s' % (self.stkexchen, self.stkexchcn)

class StockIndex(models.Model):
    '''
    stock index to stock exchange
    '''
    stkindex = models.CharField(max_length=30, blank = True, verbose_name = u'指数名称')
    exchange = models.CharField(max_length=10, blank = True, verbose_name = u'所在市场')

    def __unicode__(self):
        return u'%s %s' % (self.stkindex, self.exchange)