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
## 探究视图
1. 构建网页内容
```python
# urls.py代码
path('download.html', views.download)
# views.py代码
import csv
# Create your views here.

def download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'A', 'B', 'C'])
    return response
```
> 输入网址：http://127.0.0.1/download.html 》文件下载

2. render()语法
```
render(request,template_name,context=None,content_type=None,status=None,using=None)
```
3. 创建数据表
```
# 根据models.py生成相关的.py文件，该文件用于创建数据表
》python manage.py makemigrations
Migrations for 'index': index\migrations\0001_initial.py - Create model product
# 创建数据表
》python manage.py migrate
```
#### 备注：关于python manage.py migrate后报错
```
raise MigrationSchemaMissing("Unable to create the django_migrations table (%s)" % exc)
django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table ((1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '(6) NOT NULL)' at line 1"))

## 原因：
Django2.1不再支持MySQL5.5，必须5.6版本以上

解决办法：

二选一
（1）Django降级到2.0
`pip install Django==2.0.0 -i https://pypi.douban.com/simple`
（2）MySQL升级

## Django使用MySQL数据库
http://yshblog.com/blog/194

CREATE DATABASE django_db DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;

CREATE USER 'myDjango'@'localhost' IDENTIFIED BY 'django2019';

GRANT ALL PRIVILEGES ON django_db.* TO 'myDjango'@'localhost';
```
## 探究模板
1. 变量与标签
2. 模板继承
3. 自定义过滤器
* 新建文件夹user_defined 》__init__.py
* user_defined下新建文件夹 templatetags 》__init__.py、myfilter.py
```python
# myfilter.py
from django import template
# 注册过滤器
register = template.Library()
# 声明并定义过滤器
@register.filter
def myreplace(value, agrs):
    oldValue = agrs.split(':')[0]
    newValue = agrs.split(':')[1]
    return value.replace(oldValue, newValue)
```
```html
<!-- html里加载使用模板过滤器 -->
{% load myfilter %}
<!DOCTYPE html>
<html>
<head>
    <title>{{ title|myreplace:'首页:我的首页' }}</title>

<!-- myreplace是过滤器的函数名
'首页:我的首页'是函数参数agrs的值
函数参数value的值为模板变量title的值 -->
```
## 模型与数据库
1. ORM框架
2. Django外键（ForeignKey）
[参考Django外键（ForeignKey）操作以及related_name的作用](https://blog.csdn.net/hpu_yly_bj/article/details/78939748)
3. 新建数据库
```
mysql -u root -p

CREATE DATABASE mydjango DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci;

GRANT ALL PRIVILEGES ON mydjango.* TO 'myDjango'@'localhost';

python manage.py makemigrations

python manage.py migrate
```
4. 数据表的关系
```python
# 多对多
class Performer(models.Model):
    id = models.InterField(primary_key=True)
    name = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
class Program(models.Model):
    id = models.InterField(primary_key=True)
    name = models.CharField(max_length=20)
    performer = models.ManyToManyField(Performer)

# 更新数据
# 单条数据
Product.objects.get(id=9).update(name='华为荣耀V9')
# 多条数据
Product.objects.filter(name='荣耀V9').update(name='华为荣耀V9')
# 全表数据
Product.objects.update(name='华为荣耀V9')

# 删除数据
# 单条删除
Product.objects.get(id=1).delete()
# 多条删除
Product.objects.filter(name='华为荣耀V9').delete()
# 全表删除
Product.objects.all().delete()
```
5. 多表查询

## 表单
```
# {% csrf_token %}
1、不推荐禁用掉django中的CSRF。
2、我们可以再html页面的form表单中添加csrf_token，带着表单的请求一起发送到服务器去验证。
```
## Admin后台系统
1. 新建用户密码
```
D:\MyDjango>python manage.py createsuperuser
Username (leave blank to use 'oldkids001'): root
Email address: ******
Password:
Password (again):
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```
2. 打开数据表auth_user查看
3. index定义的模型展示在Admin后台系统中
```python
# admin.py
from django.contrib import admin
from .models import *
# Register your models here.

# 方法一
# 将模型直接注册到admin后台
admin.site.register(Product)

# 方法二
# 自定义ProductAdmin类并继承ModelAdmin
# 注册方法一，使用Python装饰器将ProductAdmin和模型Product绑定注册到后台
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id', 'name', 'weight', 'size', 'type',]
# 注册方法二
# admin.site.register(Product, ProductAdmin)
```
#### 注册报错
> django.contrib.admin.sites.AlreadyRegistered: The model Product is already registered
```python
# 解决办法：先注销
admin.site.unregister(Product)
# 还是不行
# 直接注释掉 admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id', 'name', 'weight', 'size', 'type',]
# 注册方法二
admin.site.register(Product, ProductAdmin)
# 这样就OK了
```
4. Admin的基本设置
```python
# __init__.py
# INDEX设置中文，代码编写在App(index)的__init__.py文件中
from django.apps import AppConfig
import os
# 修改app在admin后台显示名称
# default_app_config的值来自apps.py的类名
default_app_config = 'index.IndexConfig'

# 获取当前app的命名
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

# 重写类IndexConfig
class IndexConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '网站首页'

# Products设置中文，代码编写在models.py文件中
# 设置字段中文名，用于admin后台显示
class Product(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('名称',max_length=50)
    weight = models.CharField('重量',max_length=20)
    size = models.CharField('尺寸',max_length=20)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,verbose_name='产品类型')
    # 设置返回值
    def __str__(self):
        return self.name
    class Meta:
        # 如只设置verbose_name，在Admin会显示为“产品信息s”
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'

# admin.py
# 进一步完善Admin网页标题信息
# 修改title和header
admin.site.site_title = 'MyDjango后台管理'
admin.site.site_header = 'MyDjango'

# models.py
# 设置字段中文名，用于admin后台显示
class Type(models.Model):
    id = models.AutoField('序号', primary_key=True)
    type_name = models.CharField('产品类型', max_length=20)
    # 设置返回值
    def __str__(self):
        return self.type_name
```
5. 优化ProductAdmin
```python
# admin.py
class ProductAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id', 'name', 'weight', 'size', 'type',]
    # 设置搜索字段，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'name','type__type_name']
    # 设置过滤器，如有外键应使用双下划线连接两个模型的字段
    list_filter = ['name','type__type_name']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 设置时间选择器，如字段中有时间格式才可以使用
    # date_hierarchy = Field
    # 在添加新数据时，设置可添加数据的字段
    fields = ['name', 'weight', 'size', 'type']
    # 设置可读字段,在修改或新增数据时使其无法设置
    readonly_fields = ['name']
```
## Admin的二次开发
1. 通过重写ModelAdmin的方法可以实现Admin的二次开发
```python
# 重写get_readonly_fields函数，设置超级用户和普通用户的权限
def get_readonly_fields(self, request, obj=None):
    if request.user.is_superuser:
        self.readonly_fields = []
    else:
        self.readonly_fields = ['name']
    return self.readonly_fields
```
2. 设置字段格式
```python
# models.py的模型Product
from django.utils.html import format_html
class Product(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('名称',max_length=50)
    weight = models.CharField('重量',max_length=20)
    size = models.CharField('尺寸',max_length=20)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,verbose_name='产品类型')
    # 设置返回值
    def __str__(self):
        return self.name
    class Meta:
        # 如只设置verbose_name，在Admin会显示为“产品信息s”
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'
    # 自定义函数，设置字体颜色
    def colored_type(self):
        if '手机' in self.type.type_name:
            color_code = 'red'
        elif '平板电脑' in self.type.type_name:
            color_code = 'blue'
        elif '智能穿戴' in self.type.type_name:
            color_code = 'green'
        else:
            color_code = 'yellow'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.type,
        )
    # 设置admin的标题
    colored_type.short_description = '带颜色的产品类型'

# 在admin.py的ProductAdmin中添加自定义字段
# 添加自定义字段，在属性list_display添加自定义字段colored_type，colored_type来自模型Porduct
list_display.append('colored_type')
```
3. 函数get_queryset
> 根据不同用户角色设置数据的访问权限，可以将一些重要的数据进行过滤。
```python
# admin.py
# 根据当前用户名设置数据访问权限
def get_queryset(self, request):
    qs = super(ProductAdmin, self).get_queryset(request)
    if request.user.is_superuser:
        return qs
    else:
        return qs.filter(id__lt=6)
```

4. 函数formfield_for_foreignkey
> 用于在新增或修改数据的时候，设置外键的可选值。
```python
# admin.py
# 新增或修改数据时，设置外键可选值
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'type':
        if not request.user.is_superuser:
            kwargs["queryset"] = Type.objects.filter(id__lt=4)
    return super(admin.ModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

```
5. 函数save_model
```python
# admin.py
# 修改保存方法
def save_model(self, request, obj, form, change):
    if change:
        # 获取当前用户名
        user = request.user
        # 使用模型获取修改数据,pk代表具有主键属性的字段
        name = self.model.objects.get(pk=obj.pk).name
        # 使用表单获取修改数据
        weight = form.cleaned_data['weight']
        # 写入日志文件
        f = open('D://MyDjango_log.txt', 'a')
        f.write('产品：'+str(name)+'，被用户：'+str(user)+'修改'+'\r\n')
        f.close()
    else:
        pass
    # 使用super可使自定义save_model既保留父类的已有的功能并添加自定义功能。
    super(ProductAdmin, self).save_model(request, obj, form, change)
```
6. 函数delete_model
```python
def delete_model(self, request, obj):
    pass
    super(ProductAdmin, self).delete_model(request, obj)
```
7. 自定义模板
* 修改Admin模板所在路径
> cmd 输入命令pip show django即可
(\Lib\site-pageages\django\contrib\admin\templates\admin)
> 直接修改方法不提倡，推荐利用模板继承的方法实现自定义模板开发。
* 在项目中创建模板文件夹templates，在templates下依次创建文件夹admin和index
templates 》 admin 》 index 》 change_form.html
```html
{% extends "admin/change_form.html" %}
{% load i18n admin_urls static admin_modify %}
{% block object-tools-items %}
    {# 判断当前用户角色 #}
    {% if request.user.is_superuser %}
        <li>
            {% url opts|admin_urlname:'history' original.pk|admin_urlquote as history_url %}
            <a href="{% add_preserved_filters history_url %}" class="historylink">{% trans "History" %}</a>
        </li>
    {# 判断结束符 #}
    {% endif %}
    {% if has_absolute_url %}
        <li><a href="{{ absolute_url }}" class="viewsitelink">{% trans "View on site" %}</a></li>
    {% endif %}
{% endblock %}
```
## Auth认证系统
1. 内置User实现用户管理
* 创建新的APP，命名为user，并且在项目的settings.py和urls.py中配置APP的信息
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'user',
]

# 文件夹MyDjango的urls.py的URL地址配置
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls')),
    path('user/', include('user.urls'))
]

# user文件夹新建urls.py、templates文件夹添加user.html
# urls.py文件
# 设置URL地址信息
from django.urls import path
from . import views

urlpatterns = [
    path('login.html', views.loginView, name='login'),
    path('register.html', views.registerView, name='register'),
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    path('logout.html', views.logoutView, name='logout'),
]
# 上述URL地址分别对应视图函数loginView、registerView、setpasswordView和logoutView
# 参数name用来设置URL的命名，可直接在HTML模板上使用并生成相应的URL地址。
```
* user.html代码结构
* 用户登录、注册和修改密码界面
* views.py添加用户登录注册、密码修改及注销等内容
* make_password和check_password的使用


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