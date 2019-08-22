## 网站开发流程
1. 需求分析
2. 规划静态内容
3. 设计阶段
4. 程序开发阶段
5. 测试和上线
6. 维护推广

## Django
> Django采用了MTV的框架模式，即模型（Model）、模板（Template）和视图（Views）

## 安装Django
`pip install Django`

## 创建项目
`django-admin startproject MyDjango`

## 创建项目应用
`python manage.py startapp 应用名称`
* migrations 用于数据库数据的迁移
* models.py  定义映射类关联数据库，实现数据持久化，即MTV里面的模型（Model）
* views.py   逻辑处理模块，即MTV里面的视图（Views）

## 运行项目
`python manage.py runserver`

## Django配置信息
> 配置信息主要由项目的settings.py实现

## 静态资源
```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 设置根目录的静态资源文件夹public_static
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public_static'),
                    # 设置APP(index) 的静态资源文件夹index_static
                    os.path.join(BASE_DIR, 'index/index_static')]
```
## 模板路径

## 数据库配置
> 在配置MySQL之前，首先安装mysqlclient模块
`pip install mysqlclient`

## 中间件
```python
    # LocaleMiddleware： 使用中文
    'django.middleware.locale.LocaleMiddleware',
```
## URL编写规则
```python
# 根目录的urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls'))
    # URL为空，代表为网站的域名，即127.0.0.1:8000，通常是网站的首页；
    # include将该URL分发给index的urls.py处理
]

# re_path
re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2}).html',views.mydate)
?P是固定格式
<year>为变量的编写规则
[0-9]{4}是正则表达式的匹配模式，代表变量的长度为4，只允许取0-9的值。
```

## 基本操作
```
方法	       解释
get()	      获取指定条件的对象，在views.py里面有且只能有一个，否则报错
all()	      获取所有对象
filter()	  获取满足条件的所有对象 ---》对象列表
exclude()	  获取所有不满足条件的对象，也就是get()的取反
values()	  括号内有参数就是获取指定字段的结果，不写就是显示所有字段
values_list() 区别于values，是以元组的形式来表示
order_by()	  以某个字段来排列，- 是以降序排列
reverse()	  对排列好的结果取反
distinct()	  去重 models.Book.objects.all().values("price").distinct()
count()	      计算结果的数量
first()	      取出满足条件的第一个结果
last()	      取出满足条件的最后一个结果
exists()	  判断结果是否存在
delete()	  删除记录 models.Book.objects.filter(price__lte=100).delete()
update()	  修改记录 models.Book.objects.filter(title__startswith="py").update(price=120)
```
## 标签
* for
{% for item in myList %}
{{item}}
{% endfor %}
* if
{% if name="Lily" %}
{{name}}
{% elif name="Lucy" %}
{{name}}
{% else %}
{{name}}
{% endif %}

> 数据表一对一 OneToOneField
> 数据表一对多 ForeignKey
```
choices_list = [(i+1, v['type_name']) for i,v in enumerate(Type.objects.values('type_name'))]
# 可以获取下表，enumerate每次循环可以得到下表及元素
l = [] 数据表
for i, v in enumerate(l):
    print(i, v)
```

> save_m2m() 方法用于保存ManyToMany的数据模型

## 设置缓存
```python
# settings.py
CACHES = {
    # 默认缓存数据表
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        # TIMEOUT设置缓存的生命周期，以秒为单位，若为None，则永不过期
        'TIMEOUT': 60,
        'OPTIONS': {
            # MAX_ENTRIES代表最大缓存记录的数量
            'MAX_ENTRIES': 1000,
            # 当缓存到达最大数量之后，设置剔除缓存的数量
            'CULL_FREQUENCY': 3
        }
    },
    # 设置多个缓存数据表
    'MyDjango': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'MyDjango_cache_table',
    }
}
```