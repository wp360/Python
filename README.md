## 新建项目
1. 安装Django
2. 安装管理工具 django-admin
3. 输入命令
`django-admin startproject book`
## 创建项目应用
`python manage.py startapp users`
## 用serializers.Serializer方式序列化
1. 安装Django REST framework及其依赖包
`pip install djangorestframework markdown django-filter`
2. 在seetings中注册，代码如下：
```python
INSTALLED_APPS = [
    # 省略
    'users.apps.UsersConfig',
    'rest_framework'
]
```
3. 设计users的models.py，重构用户表UserProfile
```python
# models.py
from django.db import models
# Django中提供了一个AbstractUser类，我们可以用来自由的定制我们需要的model
# 首先导入AbstractUser
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    """
    用户
    """
    APIkey = models.CharField(max_length=30,verbose_name='APIkey',default='abcdefghijklmn')
    name = models.IntegerField(default=10,verbose_name='余额')
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        def __str__(self):
            return self.username
```
4. 在settings中配置用户表的继承代码
```python
AUTH_USER_MODEL = 'users.UserProfile'
```

[Django的AbstractUser：https://blog.csdn.net/lht_521/article/details/80592543](https://blog.csdn.net/lht_521/article/details/80592543)

5. 在users的models.py文件中新建书籍信息表book
```python
from datetime import datetime
from django.db import models
class Book(models.Model):
    """
    书籍信息
    """
    title = models.CharField(max_length=30,verbose_name='书名',default='')
    isbn = models.CharField(max_length=30,verbose_name='isbn',default='')
    author = models.CharField(max_length=20,verbose_name='作者',default='')
    publish = models.CharField(max_length=30,verbose_name='出版社',default='')
    rate = models.FloatField(default=0,verbose_name='豆瓣评分')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name='书籍信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

```
6. 执行数据更新命令
```
python manage.py makemigrations
python manage.py migrate
```
7. 建立一个超级用户，用户名为admin，邮箱为test@qq.com，密码为admin1234
```
python manage.py createsuperuser
Username: admin
# 省略
```

## 连接数据库，添加表数据
1. Django administration的使用，点击跳转链接：xxx/admin，输入之前建立的超级用户
2. settings.py设置
```python
# 界面改为中文版
LANGUAGE_CODE = 'zh-hans' #en-us
# 设置中国所在时区
TIME_ZONE = 'Asia/Shanghai' #UTC
```
3. admin.py中加入要注册的表，表名为Book
4. 点击添加按钮，输入对应数据

## 新建serializers.py序列化文件
```python
from rest_framework import serializers
from .models import UserProfile,Book
class BookSerializer(serializers.Serializer):
  title=serializers.CharField(required=True,max_length=100)
  isbn=serializers.CharField(required=True,max_length=100)
  author=serializers.CharField(required=True,max_length=100)
  publish=serializers.CharField(required=True,max_length=100)
  rate=serializers.FloatField(default=0)

```
## 添加视图
```python
# views.py
from .serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile,Book
class BookAPIView1(APIView):
    """
    使用Serializer
    """
    def get(self, request, format=None):
        APIKey=self.request.query_params.get("apikey", 0)
        developer=UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance=developer.money
            if balance>0:
                isbn = self.request.query_params.get("isbn", 0)
                books = Book.objects.filter(isbn=int(isbn))
                books_serializer = BookSerializer(books, many=True)
                developer.money-=1
                developer.save()
                return Response(books_serializer.data)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")

```
## 设置路由urls.py
```python
# urls.py
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from users.views import BookAPIView1

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    path('admin/', admin.site.urls),
    path('apibook1/',BookAPIView1.as_view(),name='book1'),
]

```
## POSTMAN测试api
* https://uqsjol-8080-ybkate.access.myide.io根据生成的临时链接更新
`https://uqsjol-8080-ybkate.access.myide.io/apibook1/?apikey=abcdefghijklmn&isbn=777777`

> admin.py里添加admin.site.register(UserProfile)，后台管理页面可以看到用户信息。

## 用serializers.ModelSerializer方式序列化

> 启动运行
* python manage.py runserver
`python3 manage.py runserver 0.0.0.0:8080`

#### 运行报错
`Invalid HTTP_HOST header: 'uqsjol-8080-xxfilw.access.myide.io'. You may need to add 'uqsjol-8080-xxfilw.access.myide.io' to ALLOWED_HOSTS.`
* 解决办法：
```
解决办法： 
修改项目的setting.py配置文件

将
ALLOWED_HOSTS = []
改为
ALLOWED_HOSTS = ['*']

再次运行可以成功访问了。
```

## 使用Pycharm里的Database对数据库进行可视化操作
[https://www.django.cn/article/show-13.html](https://www.django.cn/article/show-13.html)

## git 远程分支上传
git remote add origin https://github.com/wp360/Python.git

git checkout -b book

git status

git add .

git commit -m "add file"

git push

git push --set-upstream origin book