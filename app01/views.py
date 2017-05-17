# -*- coding: utf-8 -*-
import commands, os,sys
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from app01.models import Group, Host

# Create your views here.

#file
def fileview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
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
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
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
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
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
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
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
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
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

#crontab
def crontabview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    
    if request.POST:
        key = request.POST['group']
        queryset = Host.objects.filter(group_id=key).values('name','auth_user')
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                print each
                if request.POST['action'] == "create":
                    print request.POST['action']
                    if request.POST['backup'] == "True":
                        part = ["ansible ", each["name"], " -m cron -a ", "'", 'backup="True"', " name=", '"', request.POST['name'], '"', " ", request.POST['time'], " job=", '"', request.POST['job'], '"', "'", " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
			result.append(str(run_cmd))
                    else:
                        part = ["ansible ", each["name"], " -m cron -a ", "'", "name=", '"', request.POST['name'], '"', " ", request.POST['time'], " job=", '"', request.POST['job'], '"', "'", " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
			result.append(str(run_cmd))
                else:
                    if request.POST['backup'] == "True":
                        part = ["ansible ", each["name"], " -m cron -a ", "'", 'backup="True"', " name=", '"', request.POST['name'],'"', " state=absent", "'", " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
			result.append(str(run_cmd))
                    else:
                        part = ["ansible ", each["name"], " -m cron -a ", "'", "name=", '"', request.POST['name'], '"', " state=absent", "'", " -u ", each["auth_user"]]
                        cmd = ''.join(part)
                        print cmd
			run_cmd = commands.getoutput(cmd)
			result.append(str(run_cmd))
    return render(request, "crontab.html", {'result': result, 'groups': groups})

#default
def defaultview(request):
    return render_to_response("base.html")
