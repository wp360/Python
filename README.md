## 构建项目
1. 创建项目
`django-admin startproject project .`
2. 运行项目
> python manage.py runserver
3. 设置后台管理员账户
* 数据库状态与当前模型集和迁移集同步。说白了，就是将对数据库的更改，主要是数据表设计的更改，在数据库中真实执行。例如，新建、修改、删除数据表，新增、修改、删除某数据表内的字段等等。
`python manage.py migrate`
* 创建admin用户
`python manage.py createsuperuser`
* 登录后台：http://localhost:8000/admin/，登录用户名、密码为刚才输入的
4. 创建meals应用
`python manage.py startapp meals`
* [设置添加]
```python
# settings.py

INSTALLED_APPS = [
    # 省略
    'meals'
]
```
* [meals文件夹下models.py设置]
#### 注释：Django 模型是与数据库相关的，与数据库相关的代码一般写在 models.py 中。
```python
# models.py
from django.db import models

# Create your models here.

class Meals(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=500)
    people = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    preperation_time = models.IntegerField()
    image = models.ImageField(upload_to='meals/')
```
* [建立makemigrations目录]
#### 注释：相当于在该app下建立 migrations目录，并记录下你所有的关于models.py的改动
`python manage.py makemigrations`
#### 注：会出现报错
```
ERRORS:
meals.Meals.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "pip install Pillow".
meals.Meals.price: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
* 原因：官网上还没有支持Python3的PIL，使用Pillow代替PIL（python PIL 图像处理库）。
* 解决办法：
pip install Pillow
* 如果pip安装实在太慢，试试pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Pillow
```
* [makemigrations成功，会生成一个0001_initial.py文件]
* [数据状态同步操作]
`python manage.py migrate`
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, meals, sessions
Running migrations:
  Applying meals.0001_initial... OK
```
* [meals文件夹下admin.py设置]
```python
# admin.py
from django.contrib import admin

# Register your models here.

from .models import Meals

admin.site.register(Meals)
```
* [添加数据]
> Mealss 点击+Add按钮添加数据表单
* 修改models.py
```python
# models.py
    def __str__(self):
      return self.name
```
* [slug]
> slug：用于生成一个有意义（valid, meaninful）URL
#### django相关字段解释（slug）
[slug说明: https://www.cnblogs.com/ohmydenzi/p/5584846.html](https://www.cnblogs.com/ohmydenzi/p/5584846.html)
* [models.py设置添加slug]
```python

from django.utils.text import slugify

# Create your models here.

class Meals(models.Model):
    # 省略
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
      if not self.slug and self.name:
        self.slug = slugify(self.name)
      super(Meals, self).save(*args, **kwargs)


```
* [更新makemigrations目录]
`python manage.py makemigrations`
* [数据状态同步操作]
`python manage.py migrate`
* 项目重新运行
`python manage.py runserver`
* [修改名称]
```python
# models.py
    class Meta:
      verbose_name = 'meal'
      verbose_name_plural = 'meals'
```
* [django static files]
[参考文档：https://docs.djangoproject.com/en/2.2/howto/static-files/](https://docs.djangoproject.com/en/2.2/howto/static-files/)
```python
# settings.py
# 末尾添加
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# urls.py
# 省略
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

## git 远程分支上传
```
git remote add origin https://github.com/wp360/Python.git

git checkout -b resturant

git status

git add .

git commit -m "add file"

git push

git push --set-upstream origin resturant
```