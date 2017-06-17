# ansible_task  

```
系统要求：
ansible 2.3.0.0
python 2.7.10
django 1.10.0
django-formtools 2.0
django-crispy-forms 1.6.1  
```
2016-6-21  
添加登录功能， 
修改权限，  
普通用户只能查询自己添加的主机和组。  

2016-6-20  
替换了节点管理部分  

2017-6-19  
解决了result乱码问题
```
result = [], result.appand(run_cmd)
改为：
result = '', result+=run_cmd
```

2017-6-16  
增加一键部署（result乱码问题待解决）  

2017-5-26  
linux下调试运行  

2017-5-25  
win下开发完成
