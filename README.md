# dzhops
+ 使用Django框架开发的Salt Stack Web UI
+ 这里有必要解释下，dzh是我公司简称的简拼；移动终端是我所在公司运维部门的组，并不是这套系统是在移动终端上用的。
+ 本来这个项目是我个人爱好，不过后来发现，确实能解决目前SaltStack在命令行模式下的部分缺陷；
+ 前端代码在2015年末~2016年初更换过一次，并且最新的代码并没有同步上来；

##环境：
+ RHEL 6.5 x86_64
+ salt-master 2015.5.3
+ salt-minion 2015.5.3
+ salt-api 2015.5.3（此版本已合并到主分支）
+ Django 1.6.8
+ python 2.6.6
+ MySQL 5.5
+ 网卡流量图使用rrdtool(v1.3.8)工具

## 功能介绍
1.**登陆页面**
![登陆](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/0_login.png)
2.**首页**，显示SaltMaster所在服务器及相关组件状态信息
目前监控数据及流量信息所画的图，都是通过独立脚本完成，后期会考虑集成到系统中。
![仪表盘](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/1_dashbord.png)
3.**主机列表**
进入主机列表界面，可以分成两种查看方式，一种是按照机房进行查看服务器相关信息；第二种是按照维护人员进行查看；
这些服务器相关的信息支持自动采集，由于目前写的方法只能完成采集任务，所以并没有将链接放出来，不过可以通过访问指定链接进行访问。
![主机列表](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/2_hostlist.png)
4.**SaltStack**
可完成如下功能：
+ 服务器初始化（如模块部署等）
+ 程序、配置更新
+ 日常维护操作
+ 远程命令执行
当对Minion执行操作时，会记录本次目标Minion的数量，然后与返回结果的Minion数量进行对比，找出哪些没有返回结果；当接收到返回结果后，使用bootstrap的模态框显示结果，其中蓝色表示执行成功，红色表示有失败存在，可以点击标签查看详细情况；
![模块部署](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/3_salt_deploy_enter.png)
![模块部署-返回结果](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/4_salt_deploy.png)
![模块部署-返回结果-模态框展开](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/5_salt_deploy_show.png)
![远程命令执行](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/6_remote_exec.png)
5.**MinionKeys管理**
分为以下3中情况：
+ 已经接受的keys
+ 还未接受的keys
+ 已经拒绝的keys
![MinionKeys管理](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/7_salt_key_list.png)
6.**操作记录**
可以记录每次操作执行人的账号、操作、目标、及jid，并可以通过jid查看该次操作的返回结果详细情况。
![操作记录](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/8_record.png)
![操作记录-详细](https://github.com/Hasal/dzhops_picture/blob/master/dzhops_pic/9_record_detail.png)


##计划任务设定
+ */5 * * * * /tmp/get_eth0_traffic.sh
+ */10 * * * * /var/www/dzhops/scripts/data_acquisition.py
+ */10 * * * * /var/www/dzhops/scripts/prc.py
+ */10 * * * * /var/www/dzhops/scripts/slapi.py
