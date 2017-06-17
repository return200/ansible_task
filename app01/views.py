# -*- coding: utf-8 -*-
import commands, os, sys, time
from django.shortcuts import render, render_to_response, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from app01.models import Group, Host, Task
import collections
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#file
@login_required
def fileview(request):
    cmd = ''
    result = []
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
		
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(user=user).filter(group=key).values('name','auth_user')
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
@login_required
def copyview(request):
    cmd = ''
    result = []
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
		
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
        queryset = Host.objects.filter(user=user).filter(group=key).values('name','auth_user')
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
@login_required
def shellview(request):
    cmd = ''
    result = []
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
    
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(user=user).filter(group=key).values('name','auth_user')
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
@login_required
def softwareview(request):
    cmd = ''
    result = []
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
    
    if request.POST:
        software = request.POST['name']
        print "soft %s", software
        key = request.POST['group']
        queryset = Host.objects.filter(user=user).filter(group=key).values('name','auth_user')
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
@login_required
def serviceview(request):
    cmd = ''
    result = []
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
    
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(user=user).filter(group=key).values('name','auth_user')
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
@login_required
def onekeyview(request):
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
    return render(request, "onekey.html", {'groups': groups})

#执行命令
@login_required
def runcmdview(request):
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    cmd = ''
    result = ''
    host = ''
    status = "ok"
    user = request.user.username

    if request.POST:
        task = request.POST['task']
        group = request.POST['group']
        file = request.POST['file']
        file_dir = file.split("/")[-1].split(".")[0]   #jar包名目录,win下用\\表示目录级别，linux下用/表示。       
        Task.objects.create(name=task, user=user)  #任务名写入数据库
        
        if request.user.is_superuser:
            queryset = Host.objects.filter(group=group).values('name','auth_user')   #超级用户列出所有host和auth_user
        else:
            queryset = Host.objects.filter(user=user).filter(group=group).values('name','auth_user')   #普通用户列出自己的host和auth_user
        print "runcmdview queryset:", queryset
        
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
                    print "runcmdview cmd:%s ### cmds[cmd]:%s" % (cmd, cmds[cmd])   #cmd:步骤名称，cmds[cmd]:命令内容
                    run_cmd = commands.getoutput(cmds[cmd])
                    run_result = "%s\n%s" % (cmd,run_cmd)
                    result+=run_result
                result+='\n\n'
                print "runcmdview result:", result
            Task.objects.filter(user=user).filter(name=task).update(host=host, result=result) #将主机和任务执行结果存入对应任务名称下

    return HttpResponse(status)

#获取任务运行结果
@login_required
def getcmdview(request,task):
    result = []
    user = request.user.username
    queryset = Task.objects.filter(user=user).filter(name=task).values('result')  #任务执行结果
    print "getcmdview queryset:", queryset
    
    for each in queryset:
	result.append(each['result'])
	
    return HttpResponse(result)

#节点管理：group
@login_required
def groupview(request):  
    name = ''
    comment = ''
    user = request.user.username
    
    if request.POST:
        name = request.POST['name']
        comment = request.POST['comment']
        Group.objects.create(name=name, comment=comment, user=user)
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:        
        groups = Group.objects.filter(user=user)

    print "groupview groups:", groups
    print "groupview dir(request.user):", dir(request.user)
	
    return render(request, 'group.html', {'groups': groups})

#删除组
@login_required
def delgroup(request):
    user = request.user.username
    if request.POST:
        name = request.POST['name']
        print "delgroup name:", name
        Group.objects.filter(user=user).filter(name=name).delete()
    return HttpResponseRedirect("/group/")

#节点管理：host
@login_required
def hostview(request):
    user = request.user.username
    
    if request.user.is_superuser:
        groups = Group.objects.all()
    else:
        groups = Group.objects.filter(user=user)
    
    if request.POST:
        name = request.POST['name']
        group = request.POST['group']
        print group
        auth_user = request.POST['auth_user']
        print "hostview name:%s group:%s auth_user:%s" %(name, group, auth_user)
        Host.objects.create(name=name, group=group, auth_user=auth_user, user=user)
    
    if request.user.is_superuser:
        hosts = Host.objects.all()
    else:        
        hosts = Host.objects.filter(user=user)
    
	print "hostview hosts", hosts
    return render(request, 'host.html', {'groups': groups, 'hosts': hosts})

#删除主机
@login_required
def delhost(request):
    user = request.user.username
    if request.POST:
        name = request.POST['name']
        print name
        Host.objects.filter(user=user).filter(name=name).delete()
    return HttpResponseRedirect("/host/")

#检查任务名称是否重复
@login_required
def chkduplicate(request):
    status = ''
    user = request.user.username
    print "chkduplicate request.POST['check']:", request.POST['check']
    if Task.objects.filter(user=user).filter(name=request.POST['check']):
        status = "duplicate"
    else:
        status = "unique"
    return HttpResponse(status)	

#首页
@login_required
def dashbordview(request):
    print "dashbordview request.user.username:", request.user.username
    return render(request, "base.html")

#登录
def loginview(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
#     username = ''
#     password = ''
#     user = ''
        if request.POST:
            username = request.POST['user']
            password = request.POST['passw0rd']
            error = ''
            print username, password
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                url = request.POST.get('source_url','/dashbord/')
                return redirect(url)
            else:
                return render(request, 'login.html', {'error':"用户名或密码错误"})
        else:
            return render(request, 'login.html', {'error':"用户名或密码错误"})
#注销
@login_required
def logoutview(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
#index
def indexview(request):
    return render(request, "login.html")