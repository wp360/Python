# 每日生鲜项目开发
## 项目初始化
1. 环境搭建
* python虚拟环境--virtualenv

[参考链接：https://www.cnblogs.com/technologylife/p/6635631.html](https://www.cnblogs.com/technologylife/p/6635631.html)

```
pip install virtualenv
pip install virtualenvwrapper
pip install virtualenvwrapper-win　　#Windows使用该命令

mkvirtualenv -p C:\Users\haidebaozi\AppData\Local\Programs\Python\Python36\python.exe VueShop
# 删除虚拟环境
rmvirtualenv VueShop

pip install djangorestframework

# 查看已安装
pip list

pip install django
pip install markdown django-filter
```
* 虚拟环境默认安装地址
> 计算机右键 》 属性 》 高级系统设置 》 系统变量 》  添加WORKON_HOME - E:\Evns
* 启动虚拟环境
> workon VueShop
2. 新建项目
> 打开PyCharm，File》New Project 》 Django 》 定义名称 》 选择虚拟环境（script-python.exe) 》 去掉默认的admin 》 create （新建）
3. 运行
```python
# urls.py
urlpatterns = [
    # path('admin/', admin.site.urls),
]
```
4. 修改数据库设置
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "fresh_shop",
        'USER': 'root',
        'PASSWORD': "root",
        'HOST': "127.0.0.1",
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB;' }
    }
}
```
5. Navicat新建本地数据库
6. 安装mysqlclient
* 如果报错，参考网站： https://www.lfd.uci.edu/~gohlke/pythonlibs/
7. 安装pillow (处理图片)
`pip install pillow`
8. 新建python package 》 apps
9. 移动users到apps下
10. 新建extra_apps放置第三方的包
11. 新建directory 》 media
12. 新建directory 》 db_tools
13. apps >> Mark Directory >> Sources Root
14. extra_apps >> Mark Directory >> Sources Root
15. 设置根目录
```python
# settings.py
import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

```
## 数据模型
1. 新建应用
* Tools >> Run manage.py Task...
* manage.py@FreshShop > startapp goods 回车
* 移动新建的goods文件夹到apps
* 以此类推，新建trade、user_operation
> User models设计
2. 用户数据模型
```python
# users >> models.py

```
3. settings设置
```python
# settings.py
AUTH_USER_MODEL = 'users.UserProfile'
```
> Goods models设计
4. 商品数据模型
```python
# goods >> models.py
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.


class GoodsCategory(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录", related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """

class Goods(models.Model):
    """
    商品
    """

class IndexAd(models.Model):
    """
    首页商品类别广告
    """

class GoodsImage(models.Model):
    """
    商品轮播图
    """

class Banner(models.Model):
    """
    轮播的商品
    """

class HotSearchWords(models.Model):
    """
    热搜词
    """
```
5. 第三方应用DjangoUeditor添加
6. settings设置对应app
```python
INSTALLED_APPS = [
    # 省略
    'users.apps.UsersConfig',
    'DjangoUeditor',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig'
]

```
> Trade models设计
7. 交易数据模型
> User Opration models设计
8. 用户操作数据模型
9. 创建数据表
```
python manage.py makemigrations
python manage.py migrate
```
10. 报错解决，添加`on_delete=models.CASCADE`
```
在外键值的后面加上 on_delete=models.CASCADE
原因：

在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错：
TypeError: __init__() missing 1 required positional argument: 'on_delete'
```
11. xadmin后台管理系统的配置
> 拷贝xadmin第三方应用
[下载链接: https://github.com/sshwsfc/xadmin/tree/django2](https://github.com/sshwsfc/xadmin/tree/django2)
```python
# settings.py设置
INSTALLED_APPS = [
    # 省略
    'crispy_forms',
    'xadmin'
]
```
12. 拷贝adminx.py文件到对应的应用文件（goods、trade、user_operation、user）
13. 安装相关插件
> cmd打开终端，输入命令：workon VueShop
```
安装参考：https://github.com/sshwsfc/xadmin/blob/master/requirements.txt
进入虚拟环境 > pip install django-crispy-forms django-reversion django-formtools future httplib2 six
操作excel文件，还需安装
进入虚拟环境 > pip install xlwt xlsxwriter
```
14. 更新数据库
```
python manage.py makemigrations
python manage.py migrate
```
15. 创建超级用户
* Tools >> Run manage.py Task...
> createsuperuser
```
> Username:  admin
> 邮箱:  admin@qq.com
> Warning: Password input may be echoed.
> Password:  haidebaozi
> Warning: Password input may be echoed.
> Password (again):  haidebaozi
> Bypass password validation and create user anyway? [y/N]: The password is too similar to the username.
> This password is too common.
```
## xadmin集成DjangoUeditor
[https://www.cnblogs.com/fiona-zhong/p/10233697.html](https://www.cnblogs.com/fiona-zhong/p/10233697.html)
* 关于django xadmin 后台集成UEditor 的一些注意事项
[https://blog.csdn.net/wgpython/article/details/79585205](https://blog.csdn.net/wgpython/article/details/79585205)

## render() got an unexpected keyword argument 'renderer'报错的解决办法
> 直接把报错的代码注释掉即可

## Django2.0集成xadmin管理后台遇到的错误
[https://blog.csdn.net/yuezhuo_752/article/details/87916995](https://blog.csdn.net/yuezhuo_752/article/details/87916995)

## python 关于django 2.X from django.contrib.auth.views import login
[https://www.cnblogs.com/dingjiaoyang/p/10725227.html](https://www.cnblogs.com/dingjiaoyang/p/10725227.html)

#### 参考文档
[Django用户认证模块中继承AbstractUser与AbstractBaseUser重写User表的区别](https://blog.csdn.net/weixin_30709061/article/details/94816323)

[Django文档——Model字段类型(Field Types)](https://www.cnblogs.com/linxiyue/p/3662887.html)

## 数据导入
1. db_tools下新建data文件夹添加原始数据内容
2. 新建导入代码import_category_data.py
```python
# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreshShop.settings')

import django
django.setup()

from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat["code"]
        lev2_intance.name = lev2_cat["name"]
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()

```
3. 运行
* 右键Run当前文件或者快捷键Ctrl+Shift+F10
4. 同样操作新建import_goods_data.py导入商品数据
5. settings.py设置media默认路径
```python
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```
6. urls.py设置
```python
from django.conf.urls import url, include
import xadmin
from FreshShop.settings import MEDIA_ROOT
from django.views.static import serve

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
```

## git 远程分支上传
git remote add  origin  https://github.com/wp360/Python.git

git checkout -b freshshop

git status

git add .

git commit -m "add file"

git push

git push --set-upstream origin freshshop