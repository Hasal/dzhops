# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class userList(models.Model):
    userid = models.CharField(max_length=15)
    username = models.CharField(max_length=30, blank=True)
    usermail = models.CharField(max_length=30, blank=True)
    userperm = models.CharField(max_length=200, blank=True)
    usertarg = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' %(self.userid, self.username, self.userattr, self.usertarg)