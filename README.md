
hyserver为hymp提供后台服务，使用Django开发，分成三个app(hyserver/cinema/movie)

	django-admin startproject hyserver			# 生成项目
	python manage.py runserver 0.0.0.0:8000		# 访问项目主页


hymp主要提供三个tab：

1. 电影列表及详情: 主要通过豆瓣api获取电影信息，由于微信小程序限制跨域url的数量，通过Nginx将请求转发到豆瓣即可
 
2. 影院列表及详情：列表页通过cinema app获取影院信息，影院详情页通过movie app获取当前影院上映的电影及价格信息
 
3. 个人中心：目前没有与hyserver进行交互

## hyserver

项目入口，startproject时默认生成hyserver app，三个py文件


- setting.py: 项目配置信息，如DB连接配置、语言时区等
	
		ALLOWED_HOSTS = ['*']    # 上线后配置此项，允许其他机器远程访问服务

- url.py: 配置url路径对应的响应方法

- usgi.py: 与wsgi容器通信入口


## cinema

	python manage.py startapp cinema

- /cinemas/

 根据用户当前位置按由近到远分页返回电影院信息，包括电影院id、名称、详细地址、经纬度、最低价，这些信息从cinema表直接获取，由近及远排序利用将经纬度存储为MySQL地理类型Point，然后借助SQL order by实现
	
	# 通过pymysql直接执行sql
	pip install pymysql

	# st_distance是mysql提供的地理函数，可计算两个Point之间的距离
	select id_mt, name, addr, lat_lng, min_price
    from cinema where city="上海" and min_price>0 
    order by st_distance(Point({current_lat_lon}),location) asc 
    limit 1, 10;

	# cinema表，电影院详情信息，包含各渠道电影院id, 以猫眼影院id为主键，猫眼信息相对比较全
	CREATE TABLE `cinema` (
	  `id_mt` int(11) NOT NULL,
	  `id_tb` int(255) NOT NULL DEFAULT '0',
	  `id_lm` int(255) NOT NULL DEFAULT '0',
	  `name` varchar(30) NOT NULL DEFAULT '',
	  `city` varchar(20) NOT NULL DEFAULT '',
	  `district` varchar(20) NOT NULL DEFAULT '',
	  `addr` varchar(100) NOT NULL DEFAULT '',
	  `lat_lng` varchar(50) NOT NULL DEFAULT '',
	  `location` point DEFAULT NULL,
	  `min_price` float NOT NULL DEFAULT '0',
	  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  PRIMARY KEY (`id_mt`),
	  KEY `idx_id_tb` (`id_tb`) USING BTREE,
	  KEY `idx_id_lm` (`id_lm`) USING BTREE,
	  KEY `idx_city` (`city`) USING BTREE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;

	# 城市对应关系
	CREATE TABLE `city` (
	  `id_mt` int(11) NOT NULL,
	  `id_tb` int(11) NOT NULL,
	  `id_lm` int(11) NOT NULL,
	  `g` char(255) NOT NULL,
	  `name` varchar(10) NOT NULL,
	  `fly` bit(1) NOT NULL DEFAULT b'0',
	  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  PRIMARY KEY (`id_mt`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8;


- /cinemas/serach/

提供影院搜索功能，hymp中利用baidu map sdk将用户输入的地址转换成经纬度信息，然后再利用与/cinemas一样的逻辑，返回与搜索目标位置由近到远的电影院


## movie

- /movies/?cinemaId= 

根据cinemaId获取影院在售电影信息，展示在hymp影院详情页，price表中有影院和电影信息，因此在price表中根据cinemaId找到moive_id然后从movie表获取movie详情
	
	# movie表包含各个渠道id,以豆瓣id为key,便于与电影列表页中电影对应起来
	CREATE TABLE `movie` (
	  `id_db` int(11) NOT NULL,
	  `id_mt` int(11) NOT NULL DEFAULT '0',
	  `id_tb` int(11) NOT NULL DEFAULT '0',
	  `id_lm` int(11) NOT NULL DEFAULT '0',
	  `name` varchar(20) NOT NULL DEFAULT '',
	  `type` varchar(20) NOT NULL DEFAULT '',
	  `actors` varchar(255) NOT NULL DEFAULT '',
	  `score` float NOT NULL DEFAULT '0',
	  `duration` varchar(20) NOT NULL DEFAULT '',
	  `poster` varchar(255) NOT NULL DEFAULT '',
	  `release_date` varchar(10) NOT NULL DEFAULT '',
	  `ongoing` bit(1) NOT NULL DEFAULT b'0',
	  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  PRIMARY KEY (`id_db`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8；
	
	# price表包含影院、电影、放映、各渠道价格等信息，是比价的核心
	CREATE TABLE `price` (
	  `cinema_id` int(11) NOT NULL,
	  `movie_id` int(11) NOT NULL,
	  `show_date` date NOT NULL,
	  `begin` varchar(10) NOT NULL,
	  `end` varchar(10) NOT NULL DEFAULT '',
	  `language` varchar(20) NOT NULL DEFAULT '',
	  `hall` varchar(50) NOT NULL DEFAULT '',
	  `price_mt` float NOT NULL DEFAULT '0',
	  `price_tb` float NOT NULL DEFAULT '0',
	  `price_lm` float NOT NULL DEFAULT '0',
	  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	  PRIMARY KEY (`cinema_id`,`movie_id`,`show_date`,`begin`)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8；



- /movies/{movie_id}/price/?cinemaId=

获取影院里某个电影的所有比价信息，包含所有售卖日期和售卖渠道，price表中已经包含了所有渠道售价信息，直接根据cinema_id和movie_id过滤即可


## Admin UI

利用Django Admin后台可以方便的管理个业务对象，不仅有moive/cinema/price，也有通过hyspider从各个渠道抓取过来的城市、影院、电影、价格等信息。

	python manage.py makemigrations            #根据model类产生sql脚本
	python manage.py sqlmigrate cinema 0001    #查看产生的sql脚本
	python manage.py migrate				   #执行sql脚本，生成业务表
	python manage.py createsuperuser 		   #创建管理员


## Deploy

1、安装python

	yum install lrzsz
	yum install gcc
	wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
	yum install sqlite-dev
	./configure --prefix=/usr/local/python3.6 --enable-optimizations
	make && make install 
	python -m http.server # 启用http server进行测试

2、 安装uWSGI

	pip install uwsgi
	uwsgi uwsgi.ini

uwsgin.ini配置文件

	[uwsgi]
	chdir=/root/hy/hyserver #hyserver安装路径
	module=hyserver.wsgi:application
	master=True
	socket=127.0.0.1:3031	# uWSGI服务端口，与nginx通信
	pidfile=/tmp/hyserver.pid
	vacuum=True
	max-requests=5000
	daemonize=/var/log/hyserver.log
	py-autoreload=1


3、安装Nginx

	wget http://nginx.org/download/nginx-1.14.0.tar.gz
	yum -y install pcre-devel zlib-devel openssl openssl-devel
	./configure --with-http_ssl_module --prefix=/usr/local/nginx
	make && make install
	/usr/local/nginx/sbin/nginx -s reload #重启Nginx

nginx.conf配置文件
	
	#user配置成nginx启动用户，默认配置为nobody，不更改可能会报权限相关错误
	user  root;	
	worker_processes  1;
	
	events {
	    worker_connections  1024;
	}
	
	http {
	    include       mime.types;
	    default_type  application/octet-stream;
	
	    sendfile        on;
	    keepalive_timeout  65;
		
		server {
			listen       443;	# https默认端口
			server_name  www.jinjiating.xyz;
			ssl on;
			ssl_certificate 1_jinjiating.xyz_bundle.crt; # https证书，在借助tecent云生成，与nginx.conf同目录
			ssl_certificate_key 2_jinjiating.xyz.key;    # https证书
			ssl_session_timeout  5m;
			ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
			ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
			ssl_prefer_server_ciphers  on;
	
			# 与uWSGI通信配置
			location / {
				uwsgi_pass  127.0.0.1:3031;
				include     uwsgi_params;
				uwsgi_param UWSGI_CHDIR /root/hyserver;
				uwsgi_param UWSGI_SCRIPT hyserver.wsgi;
			}
			
			# 静态文件映射
			location  /static  {
				alias  /root/hy/hyserver/static;
			}
			
			# 转发豆瓣api请求
			location /db/ {
				proxy_pass https://api.douban.com/;
				proxy_redirect     off;
				proxy_set_header   Referer          "https://www.douban.com";
			}
	    }
	}



## static 文件

python manage.py runserver执行后，访问admin时需要的css等静态文件会从Django安装目录中查找，但部署到线上通过Nginx代理请求时静态文件找不到，需要将static文件收集到项目目录下，然后配置Nginx静态文件映射路径。

	
1、 settings.py中配置静态文件路径，STATIC_ROOT = BASE_DIR + '/static'

2、 执行python manage.py collectstatic，收集静态文件到STATIC_ROOT下

3、 Nginx配置文件server中配置/static映射

	    location  /static  {
            alias  /root/hy/hyserver/static;
        }



## GitHub

[https://github.com/improvejin/hyserver](https://github.com/improvejin/hyserver)