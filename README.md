## 建站基础
1. 安装Django
`pip install Django`
2. 测试是否安装
* cmd > python > 交互解释器 > 输入：
```
>>> import django
>>> django.__version__
'2.2.3'
```
3. 创建项目
```
C:\Users\用户名>d:

D:\>django-admin startproject MyDjango

D:\>cd MyDjango

D:\MyDjango>code .

```
4. 目录结构
```
+-- MyDjango
|   +-- MyDjango // 文件夹
|   |   +-- __init__.py // 初始化文件
|   |   +-- settings.py // 项目配置文件
|   |   +-- urls.py     // 项目的URL设置，网站的地址信息
|   |   +-- wsgi.py     // Python服务器网关接口
|   +-- manage.py // 命令行工具
```
5. 新建项目应用
* 网站首页
`python manage.py startapp index`
* 用户中心
`python manage.py startapp user`
6. index项目目录
```
+-- MyDjango
|   +-- index // 文件夹
|   |   +-- migrations  // 用于数据库的迁移
|   |   |   +-- __init__.py // 初始化文件
|   |   +-- __init__.py // 初始化文件
|   |   +-- admin.py    // 当前APP的后台管理系统
|   |   +-- apps.py     // 当前APP的配置信息
|   |   +-- models.py   // 定义映射类关联数据库，实现数据持久化，即MTV里面的模型（Model）
|   |   +-- tests.py    // 自动化测试的模块
|   |   +-- views.py    // 逻辑处理模块，即MTV里面的视图（Views）
```
7. 运行
`python manage.py runserver 80`
## 配置信息
1. 静态资源设置
```python
# 设置根目录的静态资源文件夹public_static
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public_static'),
# 设置APP(index) 的静态资源文件夹index_static
os.path.join(BASE_DIR, 'index/index_static')]
```
```
index >> index_static >> index_pic.png
http://localhost/static/index_pic.png
public_static >> public_pic.png
http://localhost/static/public_pic.png
```
## 数据库配置
1. 安装
`pip install mysqlclient`
> 可能需要更新pip：python -m pip install --upgrade pip
2. 测试是否安装
* cmd > python > 交互解释器 > 输入：
```
>>> import MySQLdb
>>> MySQLdb.__version__
'1.3.12'
```
3. 配置MySQL数据库连接信息
```python
# settings.py
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'POST': '3306'
    }
}
```
4. 多个数据库设置
```python
DATABASES = {
    # 第一个数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'POST': '3306'
    },
    # 第二个数据库
    'MyDjango': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyDjango_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'POST': '3306'
    },
    # 第三个数据库
    'my_sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### 注意：
1. 版本低
```
安装mysqlclient可能会出现版本过低报错，需要对源码进行修改，在Python的安装目录下找到base
（C:\Users\用户名\AppData\Local\Programs\Python\Python36-32\Lib\site-packages\django\db\backends\mysql\base.py）
```
```python
# 注释掉这两句
# if version < (1, 3, 13):
#     raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```
2. mysqlclient 提示Microsoft Visual C++ 14.0 is required问题
> 解决办法： 离线安装
`pip install mysqlclient-1.4.2-cp36-cp36m-win32.whl`
[参考：https://blog.csdn.net/moshowgame/article/details/82013080](https://blog.csdn.net/moshowgame/article/details/82013080)

## 中间件
```python
MIDDLEWARE = [
    # 使用中文
    'django.middleware.locale.LocaleMiddleware',
```

## 编写URL规则
1. URL(Uniform Resource Locator, 统一资源定位符)
> URLconf
2. urls.py
```python
# 根目录的urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    # 配置简单URL
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
]

# 上述代码设定了两个URL地址，分别是Admin站点管理和首页地址

# index的urls.py
from django.urls import path,
from . import views
urlpatterns = [
    # 配置简单URL
    path('', views.index)
]

# index的views.py
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello world")
```

#### 注：新建数据库
```
打开mysql命令对话框

输入 create database 数据库名称 default charset=utf8;
```

## git 远程分支上传
```
git remote add origin https://github.com/wp360/Python.git

git checkout -b myDjango

git status

git add .

git commit -m "add file"

git push

git push --set-upstream origin myDjango
```