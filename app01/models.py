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
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'组名')
    comment = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'备注')
    user = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'操作用户')
	
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '分组管理'
        verbose_name_plural = '分组管理'
	ordering = ['name']

class Host(models.Model):
    name = models.GenericIPAddressField(max_length=255, blank=False, null=False, verbose_name=u'主机地址')
    group = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'组别')
    auth_user = models.CharField(max_length=10, blank=False, null=False, default="root", verbose_name=u'认证用户')
    user = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'操作用户')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = '主机管理'
	ordering = ['group']

class Task(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'任务描述')
    group = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'任务组别')
    file = models.CharField(max_length=50, blank=False, null=False, verbose_name=u'项目文件')
    # host = models.TextField(blank=False, null=False, verbose_name=u'任务主机')
    task_status = models.CharField(max_length=50, blank=False, null=False, default=u"待部署", verbose_name=u'任务状态')
    run_status = models.CharField(max_length=50, blank=False, null=False, default='info', verbose_name=u'任务状态')
    button_status = models.CharField(max_length=8, verbose_name=u'按钮状态')
    result = models.TextField(blank=False, null=False, verbose_name=u'执行结果')
    user = models.CharField(max_length=20, blank=False, null=False, verbose_name=u'操作用户')

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '任务管理'
        verbose_name_plural = '任务管理'
	ordering = ['group']
#class Copy(models.Model):
#    file = models.FileField(upload_to='file')
