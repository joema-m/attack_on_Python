## 源码安装

下载地址：https://www.mongodb.com/try/download/community

选择对应的压缩包版本

<img src="..\img\mongodb_download.png" alt="mongodb_download" style="zoom:90%;" />

下载后解压，然后移动到安装自定义软件的目录

(本人是以`root`用户操作的，所以没加`sudo`)

```sh
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-4.4.0.tgz
tar -zxvf mongodb-linux-x86_64-rhel70-4.4.0.tgz
mkdir /usr/local/mongodb
mv mongodb-linux-x86_64-rhel70-4.4.0 /usr/local/mongodb
cd /usr/local/mongodb/mongodb-linux-x86_64-rhel70-4.4.0
mv * ../
cd ..
rm -r mongodb-linux-x86_64-rhel70-4.4.0

# 以上完成后，目录如下
[root@majun mongodb]# pwd
/usr/local/mongodb
[root@majun mongodb]# ll
total 136
drwxr-xr-x 2 root root  4096 Sep  5 15:34 bin
-rw-r--r-- 1 root root 30608 Sep  3 00:00 LICENSE-Community.txt
-rw-r--r-- 1 root root 16726 Sep  3 00:00 MPL-2
-rw-r--r-- 1 root root  1977 Sep  3 00:00 README
-rw-r--r-- 1 root root 75685 Sep  3 00:00 THIRD-PARTY-NOTICES
```



## 下面来配置MongoDB

### 首先将MongoDB可执行文件添加到PATH路径

```sh
vim /etc/profile
# 在末尾添加以下内容
export PATH=/usr/local/mongodb/bin:$PATH
# 保存退出
source /etc/profile
```



### 创建数据库文件目录和日志目录

默认情况下 MongoDB 启动后会初始化以下两个目录：

- 数据存储目录：`/var/lib/mongodb`
- 日志文件目录：`/var/log/mongodb`

```sh
mkdir -p /var/lib/mongo
mkdir -p /var/log/mongodb
```

### 创建MongoDB配置文件

```sh
mkdir /etc/mongodb
vim /etc/mongodb/mg.conf
```

添加以下内容,

```sh
dbpath = /var/lib/mongo
logpath = /var/log/mongodb/mongodb.log
port = 27017
logappend = true
fork = true
bind_ip = 0.0.0.0
auth = true
```

### 添加防火墙开放端口

```sh
iptables -I INPUT -p tcp --dport 27017 -j ACCEPT
/etc/rc.d/init.d/iptables save

或
firewall-cmd --zone=public --add-port=27017/tcp --permanent
irewall-cmd --reload
```



### 创建MongoDB启动配置文件

```sh
vim /usr/lib/systemd/system/mongodb.service
```

添加以下内容

```sh
[Unit]
Description=mongodb
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
RuntimeDirectory=mongodb
# 注意下面的路径
PIDFile=/var/lib/mongo/mongod.lock
ExecStart=/usr/local/mongodb/bin/mongod --config /etc/mongodb/mg.conf
ExecStop=/usr/local/mongodb/bin/mongod --shutdown --config /etc/mongodb/mg.conf
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```



### 启动MongoDB并加入开机启动

```sh
systemctl daemon-reload
systemctl start mongodb
systemctl enable mongodb
```

## 测试

### 创建用户

```sh
mongo

use admin

db.createUser({
	user:"root",
	pwd:"password",
	roles:[{role:"root",db:"admin"}]
})
```

### 本地连接测试

```sh
mongo mongodb://root:password@localhost
```

### 远程连接测试

```sh
mongo mongodb://root:password@ip地址
```



参考：

https://www.runoob.com/mongodb/mongodb-linux-install.html

https://blog.51cto.com/andyxu/2317805

