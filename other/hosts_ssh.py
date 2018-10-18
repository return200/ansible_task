#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.shortcuts import render
from app01.models import Group, Host
import os, sys
import subprocess

# host_file = '/etc/hosts'  #'/etc/%s' % (request.POST[request.user.username])
# group_name = '[testtttt]'   #'[%s]\n' % (request.POST['group'])


#执行ssh
def do_ssh(request):
    info = ''
    if request.POST:
        script = sys.path[0]+'/other/auto_ssh.sh'
        user = request.POST['auth_user']
        ip = request.POST['name']
        passwd = request.POST['passw0rd']
        
        if os.path.exists(script):
          cmd=' '.join([script, user, ip, passwd])
          print 'do_ssh cmd:%s' % (cmd)
          run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
          (output, err) = run.communicate()
          print 'output: %s ,err:%s' % (output,err)
          if 'Permission denied' in output:
            info = '用户名或密码错误'
          elif '无法创建目录' in output:
            info = '目标主机家目录权限错误'
          elif 'No route to host' in output:
            info =  '主机不可达'
          elif 'Now try logging into' in output:
            info = 'Success'
        else:
          info = '%s Not Found' % script
    return info

if __name__ == '__main__':
    print 'Only Run By import'

#追加hosts文件，思路：先将信息存到数据库，再触发数据库生成文件。
# group_list = Group.object.all()
# for each in group_list:
    # host_info = Host.object.filter(group=each['name']).values('name', 'auth_user')
    # info = '''
        # [%s]
        # %s
        # 'ansible_ssh_user=%s'
        # 'ansible_ssh_port=2048'
    # ''' % (each['name'], host_info['name'], host_info['auth_user'])
    # f = file(host_file, 'a+')
    # f.writelines(info)
    # f.close()
    
    
    
