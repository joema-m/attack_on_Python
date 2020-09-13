# CentOS安装MySQL

之前也装过好几次MySQL，每次或多或少都会出现一些小问题，今天来完整地记录下安装过程。



## 1.YUM安装

参考：https://juejin.im/post/6844903870053761037

### 1.0 删除已安装的MySQL

检查MySQL

```sh
 rpm -qa|grep mysql
```

删除MySQL

如果不存在（上面检查结果返回空）则跳过步骤

```sh
 rpm -e --nodeps xxx
```



### 1.1 添加MySQL Yum Repository

> 从CentOS 7开始，MariaDB成为Yum源中默认的数据库安装包。也就是说在CentOS 7及以上的系统中使用yum安装MySQL默认安装的会是MariaDB（MySQL的一个分支）。如果想安装官方MySQL版本，需要使用MySQL提供的Yum源。

下载MySQL源

官网地址：[dev.mysql.com/downloads/r…](https://dev.mysql.com/downloads/repo/yum/)

查看系统版本：

```sh
 cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)
```

选择对应的版本进行下载，例如CentOS 7当前在官网查看最新Yum源的下载地址为： [dev.mysql.com/get/mysql80…](https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm)

```sh
wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
```

安装MySQL源

```sh
rpm -Uvh mysql80-community-release-el7-3.noarch.rpm
```

检查是否安装成功

执行成功后会在`/etc/yum.repos.d/`目录下生成两个repo文件`mysql-community.repo`及 `mysql-community-source.repo`

并且通过`yum repolist`可以看到mysql相关资源

```sh
yum repolist enabled | grep "mysql.*-community.*"
!mysql-connectors-community/x86_64 MySQL Connectors Community                108
!mysql-tools-community/x86_64      MySQL Tools Community                      90
!mysql80-community/x86_64          MySQL 8.0 Community Server                113
```



### 1.2 选择MySQL版本

查看当前MySQL Yum Repository中所有MySQL版本（每个版本在不同的子仓库中）

```sh
yum repolist all | grep mysql
```

切换版本，这里安装mysql5.7

```sh
yum-config-manager --disable mysql80-community
yum-config-manager --enable mysql57-community
```

##### 检查当前启用的MySQL仓库

```sh
yum repolist enabled | grep mysql
```



### 1.3 安装MySQL

```sh
yum install mysql-community-server
```

该命令会安装MySQL服务器 (mysql-community-server) 及其所需的依赖、相关组件，包括mysql-community-client、mysql-community-common、mysql-community-libs

### 1.4 启动MySQL

```sh
# 启动
systemctl start mysqld
# 开机启动
systemctl enable mysqld
systemctl daemon-reload
```



### 1.5 修改密码

MySQL第一次启动后会创建超级管理员账号`root@localhost`，初始密码存储在日志文件中：

```sh
grep 'temporary password' /var/log/mysqld.log
```

修改默认密码

```sh
mysql -uroot -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'your password';
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

出现上面的提示是因为密码太简单了，解决方法如下：

1. 使用复杂密码，MySQL默认的密码策略是要包含数字、字母及特殊字符；

2. 如果只是测试用，不想用那么复杂的密码，可以修改默认策略，即`validate_password_policy`（以及`validate_password_length`等相关参数），使其支持简单密码的设定

   可以看在这里：https://www.jianshu.com/p/5779aa264840

   ```mysql
   # 更改密码策略为LOW
   set global validate_password_policy=0;
   # 更改密码长度
   set global validate_password_length=0;
   ```

3. 修改配置文件`/etc/my.cnf`，添加`validate_password=OFF`，这样一来就不需要密码了。保存并重启MySQL

4. 再次修改密码

### 1.6 允许root远程访问

```mysql
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'your password' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```

### 1.7 设置编码为utf8

查看编码

```mysql
mysql> SHOW VARIABLES LIKE 'character%';
```

设置编码

编辑/etc/my.cnf，[mysqld]节点增加以下代码：

```
[mysqld]
character_set_server=utf8
init-connect='SET NAMES utf8'
```



