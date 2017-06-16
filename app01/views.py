# -*- coding: utf-8 -*-
import commands, os, sys, time
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
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

#onekey
# def onekeyview(request):
    # date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # groups = Group.objects.all()
    # cmd = ''
    # result = []
    # dir = "/mnt/upload/"    #win下路径要用\\代表目录级别，linux下则用/
    # if not dir:
        # os.makedirs(dir)
    # if request.POST:
        # myFile = request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
# #        if not myFile:
# #            error = "no files for upload!"
# #            return render(request, "copy.html", {'error':error})  
        # destination = open(os.path.join(dir, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        # for chunk in myFile.chunks():      # 分块写入文件  
            # destination.write(chunk)  
        # destination.close()
        # file_path = dir + myFile.name
        # print file_path
        # project = myFile.name.split(".")[0]
        # key = request.POST['group']
        # queryset = Host.objects.filter(group_id=key).values('name','auth_user')
        
        # if not queryset:
            # return HttpResponse('no hosts found!')
        # else:
            # count = 0
            # for each in queryset:
		# result.append("\n>>>>"+each['name'])
                # cmds = collections.OrderedDict()
                # cmds[u'停止tomcat服务'] = "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /usr/local/jre/bin/java |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"'+" -u "+each['auth_user']
                # cmds[u'备份项目目录'] = "ansible "+each['name']+" -m shell -a "+'"'+"cp -r /mnt/tomcat/webapps/"+project+" /mnt/tomcat/backup/"+project+"-"+date+'"'+" -u "+each['auth_user']
                # cmds[u'删除项目目录'] = "ansible "+each['name']+" -m file -a "+'"'+"dest=/mnt/tomcat/webapps/"+project+" state=absent"+'"'+" -u "+each['auth_user']
                # cmds[u'分发jar包'] = "ansible "+each['name']+" -m copy -a "+'"'+"src=/mnt/"+myFile.name+" dest=/mnt/tomcat/webapps/"+'"'+" -u "+each['auth_user']
                # cmds[u'启动tomcat服务'] = "ansible "+each['name']+" -m service -a "+'"'+"name=tomcat state=started"+'"'+" -u "+each['auth_user']
                

# #                cmds = (
# ##                "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /usr/local/jre/bin/java |grep -v grep |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"',
# #                "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /jre/bin/java |grep -v grep |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"',
# #                "ansible "+each['name']+" -m shell -a "+'"'+"cp -r /mnt/tomcat/webapps/"+project+" /mnt/tomcat/backup/"+project+"-"+date+'"'+" -u "+each['auth_user'],
# #                "ansible "+each['name']+" -m file -a "+'"'+"dest=/mnt/tomcat/webapps/"+project+" state=absent"+'"',
# #                "ansible "+each['name']+" -m copy -a "+'"'+"src="+file_path+" dest=/mnt/tomcat/webapps/"+'"',
# #                "ansible "+each['name']+" -m service -a "+'"'+"name=tomcat state=started"+'"',
# #                )          
                
                # for cmd in cmds:
		    # print cmd, "###", cmds[cmd]
		    # run_cmd = commands.getoutput(cmds[cmd])
                    # run_result = "%s\n%s" % (cmd,run_cmd)
		    # result.append(str(run_result))
# ##                cmd = ''.join(list)
# ##                print cmd
# #		    run_cmd = commands.getoutput(cmd)
# #		    result.append(str(run_cmd))
    # return render(request, "onekey.html", {'result': result, 'groups': groups})


def onekeyview(request):
    groups = Group.objects.all()
    return render(request, "onekey.html", {'groups': groups})
	
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
#         file_name = file_dir+".war" #jar包名
       
        
        Task.objects.create(name=task)  #任务名写入数据库
        
        queryset = Host.objects.filter(group_id=group).values('name','auth_user')   #列出host和auth_user
        
        if not queryset:
            return HttpResponse('no hosts found!')
        else:
            for each in queryset:
                result = result+">>>>"+each['name']
                host = host+each['name']+" "
                cmds = collections.OrderedDict()
                cmds[u'\n[ 停止tomcat服务 ]'] = "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /usr/local/jre/bin/java |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 备份项目目录 ]'] = "ansible "+each['name']+" -m shell -a "+'"'+"cp -r /mnt/tomcat/webapps/"+file_dir+" /mnt/tomcat/backup/"+file_dir+"-"+date+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 删除项目目录 ]'] = "ansible "+each['name']+" -m file -a "+'"'+"dest=/mnt/tomcat/webapps/"+file_dir+" state=absent"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 分发jar包 ]'] = "ansible "+each['name']+" -m copy -a "+'"'+"src="+file+" dest=/mnt/tomcat/webapps/"+'"'+" -u "+each['auth_user']
                cmds[u'\n\n[ 启动tomcat服务 ]'] = "ansible "+each['name']+" -m service -a "+'"'+"name=tomcat state=started"+'"'+" -u "+each['auth_user']
		for cmd in cmds:
		    print cmd, "###", cmds[cmd]	#cmd:步骤名称，cmds[cmd]:命令内容
		    run_cmd = commands.getoutput(cmds[cmd])
                    run_result = "%s\n%s" % (cmd,run_cmd)
		    result+=run_result
		result+='\n\n'
		print result
		Task.objects.filter(name=task).update(host=host, result=result) #主机，任务执行结果存入对应任务名称下
#		Task.objects.create(name=task, host=hosts, result=result)
		
    return HttpResponse(status)
	
def getcmdview(request,task):
    result = []
#    task = task
#     task = request.POST['task'] #任务名称
    queryset = Task.objects.filter(name=task).values('result')  #任务执行结果
    
    print queryset
    
    for each in queryset:
	result.append(each['result'])
##         unicode转码中文
#        foo = each['result']
#        print foo
#        bar = foo[7:len(foo)]
#        rlt = bar.decode('unicode-escape').encode('utf-8')
#        result.append(rlt)
#	 print result
##         转码结束
    return HttpResponse(result)
	
	
	
	
#default
def defaultview(request):
    return render_to_response("base.html")
