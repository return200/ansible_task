# -*- coding: utf-8 -*-
import commands, os, sys, time
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse, HttpResponseRedirect
from app01.models import Group, Host, Task
import collections

# Create your views here.

#file
def fileview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                if request.POST['params']:
                    if request.POST['action']=="modify":
                        part = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " ", request.POST['params'], '"', " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
                        result.append(str(run_cmd))
                    else:
                        part = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " state=" , request.POST['action'], " ", request.POST['params'], '"', " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
                        result.append(str(run_cmd))
                else:
                    part = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " state=" , request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(part)
                    print cmd
		    run_cmd = commands.getoutput(cmd)
		    result.append(str(run_cmd))
    return render(request, "file.html", {'result': result, 'groups': groups})

#copy
def copyview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    dir = "/mnt/upload/"    #win下路径要用\\代表目录级别，linux下则用/
    if not os.path.isdir(dir):
        os.makedirs(dir)
    if request.POST:
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!")  
        destination = open(os.path.join(dir, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()
        file_path = dir + myFile.name
        print file_path
        
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                part = ["ansible ", each["name"], " -m copy -a ", '"', "src=", file_path, " dest=", request.POST['dest'], '"', " -u ", each["auth_user"]]
                cmd = ''.join(part)
                print cmd
		run_cmd = commands.getoutput(cmd)
		result.append(str(run_cmd))
    return render(request, "copy.html", {'result': result, 'groups': groups})

#shell
def shellview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                print each
                part = ["ansible ", each["name"], " -m shell -a ", '"', request.POST['cmd'], '"', " -u ", each["auth_user"]]
                cmd = ''.join(part)
                print cmd
		run_cmd = commands.getoutput(cmd)
		result.append(str(run_cmd))
    return render(request, "shell.html", {'result': result, 'groups': groups})

#software
def softwareview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    
    if request.POST:
        software = request.POST['name']
        print "soft %s", software
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                print each
                for every in software.split(','):
                    print every.strip()
                    part = ["ansible ", each["name"], " -m ", request.POST['method'], " -a ", '"', "name=", every.strip(), " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(part)
                    print cmd
		    run_cmd = commands.getoutput(cmd)
		    result.append(str(run_cmd))
    return render(request, "software.html", {'result': result, 'groups': groups})

#service
def serviceview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                print each
                if request.POST['pattern']:
                    part = ["ansible ", each["name"], " -m service -a ", '"', "name=", request.POST['name'], " pattern=", request.POST['pattern'], " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(part)
                    print cmd
		    run_cmd = commands.getoutput(cmd)
		    result.append(str(run_cmd))
                else:
                    part = ["ansible ", each["name"], " -m service -a ", '"', "name=", request.POST['name'], " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(part)
                    print cmd
		    run_cmd = commands.getoutput(cmd)
		    result.append(str(run_cmd))
    return render(request, "service.html", {'result': result, 'groups': groups})

#返回访问的页面-->页面添加任务，通过ajax实现不刷新页面执行命令（runcmdview）-->同样通过ajax获取命令执行结果(getcmdview)
def onekeyview(request):
    groups = Group.objects.all()
    return render(request, "onekey.html", {'groups': groups})

#执行命令	
def runcmdview(request):
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    groups = Group.objects.all()
    cmd = ''
    result = ''
    host = ''
    status = "ok"
    if request.POST:
        task = request.POST['task']
        group = request.POST['group']
        file = request.POST['file']
        file_dir = file.split("/")[-1].split(".")[0]   #jar包名目录,win下用\\表示目录级别，linux下用/表示。       
        Task.objects.create(name=task)  #任务名写入数据库
        queryset = Host.objects.filter(group=group).values('name','auth_user')   #列出host和auth_user
        
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                result = result+">>>>"+each['name']
                host = host+each['name']+" "
                cmds = collections.OrderedDict()
                cmds[u'\n[ 停止 tomcat 服务 ]'] = "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /jre/bin/java |grep -v grep |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 备份项目目录 ]'] = "ansible "+each['name']+" -m shell -a "+'"'+"cp -r /mnt/tomcat/webapps/"+file_dir+" /mnt/tomcat/backup/"+file_dir+"-"+date+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 删除项目目录 ]'] = "ansible "+each['name']+" -m file -a "+'"'+"dest=/mnt/tomcat/webapps/"+file_dir+" state=absent"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 分发 jar 包 ]'] = "ansible "+each['name']+" -m copy -a "+'"'+"src="+file+" dest=/mnt/tomcat/webapps/"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 启动 tomcat 服务 ]'] = "ansible "+each['name']+" -m service -a "+'"'+"name=tomcat state=started"+'"'+" -u "+each['auth_user']
		for cmd in cmds:
		    print cmd, "###", cmds[cmd]	#cmd:步骤名称，cmds[cmd]:命令内容
		    run_cmd = commands.getoutput(cmds[cmd])
                    run_result = "%s\n%s" % (cmd,run_cmd)
		    result+=run_result
		result+='\n\n'
		print result
		Task.objects.filter(name=task).update(host=host, result=result) #将主机和任务执行结果存入对应任务名称下
		
    return HttpResponse(status)

#获取任务运行结果
def getcmdview(request,task):
    result = []
    queryset = Task.objects.filter(name=task).values('result')  #任务执行结果
    print queryset
    
    for each in queryset:
	result.append(each['result'])
	
    return HttpResponse(result)

#节点管理：group
def groupview(request):  
    name = ''
    comment = ''
    
    if request.POST:
        name = request.POST['name']
        comment = request.POST['comment']
        Group.objects.create(name=name,comment=comment)
    
    groups = Group.objects.all()
    print groups
	
    return render(request, 'group.html', {'groups': groups})

#删除组
def delgroup(request):
    if request.POST:
        name = request.POST['name']
        print name
        Group.objects.filter(name=name).delete()
    return HttpResponseRedirect("/group/")

#节点管理：host
def hostview(request):
    groups = Group.objects.all()
    name = ''
    group = ''
    auth_user = ''
    
    if request.POST:
        name = request.POST['name']
        group = request.POST['group']
        print group
        auth_user = request.POST['auth_user']
        Host.objects.create(name=name, group=group, auth_user=auth_user)
    hosts = Host.objects.all()
    print hosts
    return render(request, 'host.html', {'groups': groups, 'hosts': hosts})

#删除主机
def delhost(request):
    if request.POST:
        name = request.POST['name']
        print name
        Host.objects.filter(name=name).delete()
    return HttpResponseRedirect("/host/")

#检查任务名称是否重复
def chkduplicate(request):
    status = ''
    print request.POST['check']
    if Task.objects.filter(name=request.POST['check']):
        status = "duplicate"
    else:
        status = "unique"
    return HttpResponse(status)	

#default
def defaultview(request):
    return render_to_response("base.html")
