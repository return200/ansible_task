# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import CharField

import sys
from django.contrib.admin.utils import help_text_for_field
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.
class Group(models.Model):
    name = models.CharField(unique=True, max_length=10, blank=False, null=False, verbose_name=u'组名')
    comment = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'备注')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '分组管理'
        verbose_name_plural = '分组管理'

class Host(models.Model):
    name = models.GenericIPAddressField(unique=True, max_length=255, blank=False, null=False, verbose_name=u'主机地址')
    group = models.ForeignKey(Group, blank=False, null=False, to_field='name', verbose_name=u'组名')
    auth_user = models.CharField(max_length=10, blank=False, null=False, default="root", verbose_name=u'认证用户')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = '主机管理'

class Task(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False, verbose_name=u'任务描述')
    host = CharField(max_length=21485, blank=False, null=False, verbose_name=u'任务主机')
    result = models.TextField(blank=False, null=False, verbose_name=u'执行结果')

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '任务管理'
        verbose_name_plural = '任务管理'
#class Copy(models.Model):
#    file = models.FileField(upload_to='file')