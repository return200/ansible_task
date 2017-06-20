# -*- coding: utf-8 -*-
import commands, os, sys, time
from django.shortcuts import render, render_to_response, redirect
from django.http.response import HttpResponse, HttpResponseRedirect,\
    JsonResponse
from app01.models import Group, Host, Task
from django.views.decorators.csrf import csrf_exempt
import collections

# Create your views here.

#file
def fileview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    if request.POST:
        #list = ["ansible ", request.POST['group'], " -m copy -a ", '"', "src=", request.POST['src'], " dest=", request.POST['dest'], " status=" , request.POST['status'], '"']
        key = request.POST['group']
        queryset = Host.objects.filter(group=key).values('name','auth_user')
        if not queryset:
			error = "no hosts found!"
			return render(request, "file.html", {'error': error})
        else:
            for each in queryset:
                if request.POST['params']:
                    if request.POST['action']=="modify":
                        list = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " ", request.POST['params'], '"', " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(str(cmd))
                #        result = commands.getoutput(cmd)
                    else:
                        list = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " state=" , request.POST['action'], " ", request.POST['params'], '"', " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(str(cmd))
                #        result = commands.getoutput(cmd)
                else:
                    list = ["ansible ", each["name"], " -m file -a ", '"', "dest=", request.POST['dest'], " state=" , request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(list)
                    print cmd
                    result.append(str(cmd))
            #        result = commands.getoutput(cmd)
    return render(request, "file.html", {'result': result, 'groups': groups})

#copy
def copyview(request):
    groups = Group.objects.all()
    cmd = ''
    result = []
    dir = "E:\\upload\\"    #win下路径要用\\代表目录级别，linux下则用/
    if not dir:
        os.makedirs(dir)
    if request.POST:
        myFile = request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
#        if not myFile:
#			error = "no files for upload!"
#			return render(request, "copy.html", {'error':error})  
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
                list = ["ansible ", each["name"], " -m copy -a ", '"', "src=", file_path, " dest=", request.POST['dest'], '"', " -u ", each["auth_user"]]
                cmd = ''.join(list)
                print cmd
                result.append(str(cmd))
#        result = commands.getoutput(cmd)
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
#        list = ["ansible ", request.POST['group'], " -m shell -a ", '"', request.POST['cmd'], '"']
                list = ["ansible ", each["name"], " -m shell -a ", '"', request.POST['cmd'], '"', " -u ", each["auth_user"]]
                cmd = ''.join(list)
                print cmd
                result.append(cmd)
#        result = commands.getoutput(cmd)
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
                for each in software.split(','):
                    print each.strip()
#        list = ["ansible ", request.POST['group'], " -m shell -a ", '"', request.POST['cmd'], '"']
                    lists = ["ansible ", each["name"], " -m ", request.POST['method'], " -a ", '"', "name=", each.strip(), " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(lists)
                    print cmd
                    result.append(cmd)
#        result = commands.getoutput(cmd)
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
                    list = ["ansible ", each["name"], " -m service -a ", '"', "name=", request.POST['name'], " pattern=", request.POST['pattern'], " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(list)
                    print cmd
                    result.append(cmd)
                else:
#        list = ["ansible ", request.POST['group'], " -m shell -a ", '"', request.POST['cmd'], '"']
                    list = ["ansible ", each["name"], " -m service -a ", '"', "name=", request.POST['name'], " state=", request.POST['action'], '"', " -u ", each["auth_user"]]
                    cmd = ''.join(list)
                    print cmd
                    result.append(cmd)
#        result = commands.getoutput(cmd)
    return render(request, "service.html", {'result': result, 'groups': groups})

#crontab
def crontabview(request):
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
                if request.POST['action'] == "create":
                    print request.POST['action']
                    if request.POST['backup'] == "True":
                        list = ["ansible ", each["name"], " -m cron -a ", "'", 'backup="True"', "name=", request.POST['name'], " time=", request.POST['time'], " job=", request.POST['job'], "'", " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(cmd)
                    else:
                        list = ["ansible ", each["name"], " -m cron -a ", '"', "name=", request.POST['name'], " time=", request.POST['time'], " job=", request.POST['time'], request.POST['job'], '"', " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(cmd)
                else:
                    if request.POST['backup'] == "True":
#        list = ["ansible ", request.POST['group'], " -m shell -a ", '"', request.POST['cmd'], '"']
                        list = ["ansible ", each["name"], " -m cron -a ", '"', 'backup="True"', " name=", request.POST['name'], " state=absent", '"', " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(cmd)
                    else:
                        list = ["ansible ", each["name"], " -m cron -a ", '"', "name=", request.POST['name'], " state=absent", '"', " -u ", each["auth_user"]]
                        cmd = ''.join(list)
                        print cmd
                        result.append(cmd)
#        result = commands.getoutput(cmd)
    return render(request, "crontab.html", {'result': result, 'groups': groups})

# 返回访问的页面-->页面添加任务，通过ajax实现不刷新页面执行命令（runcmdview）-->同样通过ajax获取命令执行结果(getcmdview)
def onekeyview(request):
#     date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    groups = Group.objects.all()
#     cmd = ''
#     result = []
#     
#     dir = "E:\\upload\\"    #win下路径要用\\代表目录级别，linux下则用/
#     if not dir:
#         os.makedirs(dir)
#     if request.POST:
#         myFile = request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
# #        if not myFile:
# #            error = "no files for upload!"
# #            return render(request, "copy.html", {'error':error})  
#         destination = open(os.path.join(dir, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
#         for chunk in myFile.chunks():      # 分块写入文件  
#             destination.write(chunk)  
#         destination.close()
#         file_path = dir + myFile.name
#         print file_path
#         project = myFile.name.split(".")[0]
#         
#         key = request.POST['group']
#         queryset = Host.objects.filter(group=key).values('name','auth_user')
#         
#         if not queryset:
#             return HttpResponse('no hosts found!')
#         else:
#             for each in queryset:
#                 result.append("\n>>>>"+each['name'])
#                 cmds = collections.OrderedDict()
#                 cmds[u'停止tomcat服务'] = "ansible "+each['name']+" -m shell -a "+'"'+"ps aux |grep /usr/local/jre/bin/java |awk "+"'"+"{print \$2}"+"'"+" |xargs kill -9"+'"'+" -u "+each['auth_user']
#                 cmds[u'备份项目目录'] = "ansible "+each['name']+" -m shell -a "+'"'+"cp -r /mnt/tomcat/webapps/"+project+" /mnt/tomcat/backup/"+project+"-"+date+'"'+" -u "+each['auth_user']
#                 cmds[u'删除项目目录'] = "ansible "+each['name']+" -m file -a "+'"'+"dest=/mnt/tomcat/webapps/"+project+" state=absent"+'"'+" -u "+each['auth_user']
#                 cmds[u'分发jar包'] = "ansible "+each['name']+" -m copy -a "+'"'+"src=/mnt/"+myFile.name+" dest=/mnt/tomcat/webapps/"+'"'+" -u "+each['auth_user']
#                 cmds[u'启动tomcat服务'] = "ansible "+each['name']+" -m service -a "+'"'+"name=tomcat state=started"+'"'+" -u "+each['auth_user']
#                 
#                 for cmd in cmds:
#                     print cmd, "###", cmds[cmd]
#                     run = "%s\n%s" % (cmd,cmds[cmd])
# #                cmd = ''.join(list)
# #                print cmd
#                     result.append(str(run))
# #                print request.POST['task']
# #                task_obj = Task.objects.create(name=request.POST['task'], host=each['name'], state=1)
# #                task_obj.save()
# #                time.sleep(5)
# #        result = commands.getoutput(cmd)
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
#         file_name = file_dir+".war" #jar包名
        
        print file
        
        Task.objects.create(name=task)  #任务名写入数据库
        
        queryset = Host.objects.filter(group=group).values('name','auth_user')   #列出host和auth_user
        
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
                    print cmd, "###", cmds[cmd]
                    run = "%s\n%s" % (cmd,cmds[cmd])
#                cmd = ''.join(list)
#                print cmd
#                    result.append(str(run))
                    result+=run
#                print request.POST['task']
#                task_obj = Task.objects.create(name=request.POST['task'], host=each['name'], state=1)
#                task_obj.save()
#                time.sleep(5)
#        result = commands.getoutput(cmd)
                result+='\n\n'

            Task.objects.filter(name=task).update(host=host, result=result) #主机，任务执行结果存入对应任务名称下
    return HttpResponse(status)

#获取命令执行结果
def getcmdview(request,task):
    result = []
#    task = task
#     task = request.POST['task'] #任务名称
    queryset = Task.objects.filter(name=task).values('result')  #任务执行结果
    
    print queryset
    
    for each in queryset:
#         unicode转码中文
#         foo = each['result']
#         print foo
#         bar = foo[7:len(foo)]
#         rlt = bar.decode('unicode-escape').encode('utf-8')
#         result.append(rlt)
        result.append(each['result'])
    print result
#         转码结束
    return HttpResponse(result)
#     return render(request, 'aaa.html', {'result': result})

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
#    group_comment = Group.objects.filter(name=group_name).value('comment')
    return render(request, 'group.html', {'groups': groups})

def delgroup(request):
    if request.POST:
        name = request.POST['name']
        print name
        Group.objects.filter(name=name).delete()
    return HttpResponseRedirect("/group/")

#几点管理：host
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

# def getpersentage(request):
#     task = request.POST['task']
#     group = request.POST['group']
#     file = request.POST['file']
#     
#     print task, group, file
# #    key = request.POST['group']
# #     persentage = 0
# #     finish = Task.objects.filter(state=1)
# #     host_list = finish.filter(name='test04').count()
# #     print host_list
# #     num = Host.objects.filter(group=u'测试组01').count()
# #     print num
# #     persentage = float(host_list)/float(num)*100
# #     print persentage
# #     return HttpResponse(persentage)
#     return HttpResponse("ok")
        
# #one
# def oneview(request):
#     groups = Group.objects.all()
#     result = []
#     if request.POST:
#         result.append(u"添加成功!")
#     return render(request, "one.html", {'groups': groups, 'result':result})
# 
# def oneresultview(request):
#     groups = Group.objects.all()
#     print request.POST['id1']
#  #   data = "%s %s %s\n" % (request.POST['id1'], request.POST['id2'], request.POST['id3'])
#     
# #    f = open('e:\\task.txt', "a")
# #    f.write(data)
#  #   f.close()
# #    print request.POST['id1'], request.POST['id2'], request.POST['id3']
#     return render(request, "one.html", {'groups': groups})
# 
# #onekey
# #def onekeyview(request):
# #    groups = Group.objects.all()
# #    return render(request, "onekey.html", {'groups': groups})
# 
# #def onekey_resultview(request):
# #    groups = Group.objects.all()
# #    result = ''
# #    try:
# #        result = request.POST.iterlists()
# #        result = request.POST.lists()   #获取请求内容的列表
# #        print result
# #        print len(result)   #列表长度
# #        print result[2]
# #        print result[2][0], result[2][1][0], result[2][1][1], result[2][1][2]
# #    except:
# #        pass
#     
#    
#    
# #    return render(request, "onekey.html", {'groups': groups})

#default
def defaultview(request):
    return render_to_response("base.html")