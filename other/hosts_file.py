#!/usr/bin/env python
# -*- coding: utf8 -*-

from app01.models import Group, Host
   

def create_file(request):
    host_file = '/etc/ansible/hosts_%s' % (request.user.username)
    group_list = ''
    host_info = ''
    name_info = ''
    vars_info = ''
    
    if not request.user.is_superuser:
        group_list = Group.objects.filter(user=request.user.username).values('name')
        print group_list
        f = file(host_file, 'a+')
        f.truncate()    #清空文件

        for each in group_list:
            group_name = '[%s]\n' % (each['name'])    #组名
            f = file(host_file, 'a+')
            f.writelines(group_name)
            f.close()
            host_info = Host.objects.filter(user=request.user.username).filter(group=each['name']).values('name', 'auth_user', 'group')
            print host_info
            if host_info:
                for each_host_info in host_info:
                    name_info = '%s\n' % (each_host_info['name'])   #ip地址
                    f = file(host_file, 'a+')
                    f.writelines(name_info)
                    f.close()
                vars_info = '[%s:vars]\nansible_ssh_user=%s\n\n' % (each_host_info['group'], each_host_info['auth_user'])
                f = file(host_file, 'a+')
                f.writelines(vars_info)
                f.close()

