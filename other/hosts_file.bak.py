#!/usr/bin/env python
# -*- coding: utf8 -*-

from app01.models import Group, Host

def create_file(request):
    host_file = '/etc/ansible/%s' % (request.user.username)
    group_list = ''
    host_info = ''

    if not request.user.is_superuser:
        group_list = Group.objects.filter(user=request.user.username).values('name')
        print group_list
        f = file(host_file, 'a+')
        f.truncate()

        for each in group_list:
            info = '[%s]\n' % (each['name'])    #组名
            f = file(host_file, 'a+')
            f.writelines(info)
            f.close()
            host_info = Host.objects.filter(user=request.user.username).filter(group=each['name']).values('name', 'auth_user')
	    for each_host_info in host_info:
       	        info = '%s\n' % (each_host_info['name'])   #ip地址
       	        f = file(host_file, 'a+')
       	        f.writelines(info)
       	        f.close()
       	    info = 'ansible_ssh_user=%s\nansible_ssh_port=2048\n\n' % (each_host_info['auth_user']) #登录用户和端口
       	    f = file(host_file, 'a+')
       	    f.writelines(info)
       	    f.close()

if __name__ == '__main__':
    create_file

