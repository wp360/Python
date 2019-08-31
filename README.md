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
* 登录后台：http://localhost:8000/admin/，登录用户名、密码为刚才输入的haidebaozi2
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
* [添加菜单列表视图层]
```python
# views.py
from django.shortcuts import render
from .models import Meals
# Create your views here.

def meal_list(request):
  pass

def meal_detail(request, slug):
  pass

# 新建urls.py文件（meals文件夹下）
# urls.py
from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal_list, name='meal_list'),
    path('<slug:slug>', views.meal_detail, name='meal_detail')
]

# project文件夹下urls.py
from django.urls import path, include
# 省略

urlpatterns = [
    # 省略
    path('meals/', include('meals.urls', namespace='meals')),
]

```
* [views.py新增列表页]
```python
from django.shortcuts import render
from .models import Meals
# Create your views here.

def meal_list(request):
  meal_list = Meals.objects.all()
  context = {'meal_list': meal_list}
  return render(request, 'Meals/list.html', context)

def meal_detail(request, slug):
  pass
```
> meals >> templates >> Meals >> list.html/detail.html
```html
<!-- list.html -->
<h1>美食列表</h1>
{%  for meal in meal_list %}
  <h2>
    <a href="{% url 'meals: meal_detail' meal.slug %}">{{meal}}</a>
  </h2>
{% endfor %}
```
#### 注意：如果slug为空，会报错。所以后台添加信息时要生成slug。
```python
# views.py
# 省略

def meal_detail(request, slug):
  meal_detail = Meals.objects.get(slug=slug)
  context = {'meal_detail': meal_detail}
  return render(request, 'Meals/detail.html', context)

```
```html
<!-- detail.html -->
<h1>美食详情页</h1>
<h2>{{meal_detail}}</h2>
<p>{{meal_detail.description}}</p>
<p>{{meal_detail.people}}</p>
<p>{{meal_detail.price}}</p>
<p>{{meal_detail.preperation_time}}</p>
<img src="{{meal_detail.image.url}}" alt="">
```
## 添加模板
1. 搜索免费模板

[https://colorlib.com/wp/templates/](https://colorlib.com/wp/templates/)

2. Django项目配置/static/路径，调用css、img、js等静态文件
```
例如：
<link rel="stylesheet" href="/css/bootstrap.css">
改成：
<link rel="stylesheet" href="{% static 'site_static/css/bootstrap.css' %}">
```
3. 删除多余内容
4. 循环遍历数据
```html
{% for meal in meal_list %}
  <div class="d-block d-md-flex menu-food-item">
    <div class="text order-1 mb-3">
      <h3><a href="#">{{meal.name}}</a></h3>
      <p>{{meal.description}}</p>
    </div>
    <div class="price order-2">
      <strong>${{meal.price}}</strong>
    </div>
  </div> <!-- .menu-food-item -->
{% endfor %}
```
5. Django 模板.html中 href参数传入
```html
<a href="{% url 'meals:meal_detail' meal.slug %}">{{meal.name}}</a>
```
## Category模型
1. 添加Category模型
```python
# models.py
category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

class Category(models.Model):
  name = models.CharField(max_length=30)

  def __str__(self):
    return self.name
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
```
2. 后台添加参数
```python
from django.contrib import admin

# Register your models here.

from .models import Meals, Category

admin.site.register(Meals)
admin.site.register(Category)

```
3. 关于django 2.x版本中models.ForeignKey() 外键说明
```
ForeignKey 表示设置外健
on_delete有CASCADE、PROTECT、SET_NULL、SET_DEFAULT、SET()五个可选择的值
CASCADE：此值设置，是级联删除。
PROTECT：此值设置，是会报完整性错误。
SET_NULL：此值设置，会把外键设置为null，前提是允许为null。
SET_DEFAULT：此值设置，会把设置为外键的默认值。
SET()：此值设置，会调用外面的值，可以是一个函数。
一般情况下使用CASCADE就可以了。

null=True
null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空，即在Null字段显示为yes。
```
4. 添加分类，调整视图
```python
# meals/views.py
# 省略
from .models import Meals, Category
# 省略

def meal_list(request):
# 省略
  categories = Category.objects.all()

  context = {
# 省略
    'categories': categories
  }
# 省略

# meals/models.py
class Category(models.Model):
    # 省略

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # 省略
```
```html
<!-- list.html分类切换修改 -->
<ul class="nav site-tab-nav" id="pills-tab" role="tablist">
  <li class="nav-item">
    <a class="nav-link active" id="pills-breakfast-tab" data-toggle="pill" href="#pills-breakfast" role="tab" aria-controls="pills-breakfast" aria-selected="true">Breakfast</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-lunch-tab" data-toggle="pill" href="#pills-lunch" role="tab" aria-controls="pills-lunch" aria-selected="false">Brunch</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" id="pills-dinner-tab" data-toggle="pill" href="#pills-dinner" role="tab" aria-controls="pills-dinner" aria-selected="false">Dinner</a>
  </li>
</ul>
<!-- 改成 -->
<ul class="nav site-tab-nav" id="pills-tab" role="tablist">
  {% for category in categories %}
  <li class="nav-item">
    <a class="nav-link " id="{{category}}-tab" data-toggle="pill" href="#{{category}}" role="tab"
      aria-controls="{{category}}" aria-selected="true">{{category}}</a>
  </li>
  {% endfor %}
</ul>
<!-- 内容部分 -->
<div class="tab-content" id="pills-tabContent">
  <div class="tab-pane fade show active" id="pills-breakfast" role="tabpanel" aria-labelledby="pills-breakfast-tab">
    {% for meal in meal_list %}
      <div class="d-block d-md-flex menu-food-item">
        <div class="text order-1 mb-3">
          <h3><a href="{% url 'meals:meal_detail' meal.slug %}">{{meal.name}}</a></h3>
          <p>{{meal.description}}</p>
        </div>
        <div class="price order-2">
          <strong>${{meal.price}}</strong>
        </div>
      </div> <!-- .menu-food-item -->
    {% endfor %}
  </div>
  <div class="tab-pane fade" id="pills-lunch" role="tabpanel" aria-labelledby="pills-lunch-tab">

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Jumbo Lump Crab Stack</a></h3>
        <p>Spinach and artichokes in a creamy cheese dip with warm tortilla chips &amp; salsa.</p>
      </div>
      <div class="price order-2">
        <strong>$12.49</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Jamaican Chicken Wings</a></h3>
        <p>Crisp tortilla and plantain chips covered with lightly spiced ground beef, melted cheese, pickled jalapeños, guacamole, sour cream and salsa.</p>
      </div>
      <div class="price order-2">
        <strong>$15.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Bahamian Seafood Chowder</a></h3>
        <p>A heaping mountain of rings, handmade with Panko breading and shredded coconut flakes.</p>
      </div>
      <div class="price order-2">
        <strong>$10.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Grilled Chicken &amp; Tropical Fruit on Mixed Greens</a></h3>
        <p>Lobster and tender shrimp, with onions, sweet peppers, spinach and our three cheese blend. Griddled and served with tomato salsa and sour cream.</p>
      </div>
      <div class="price order-2">
        <strong>$12.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

  </div>
  <div class="tab-pane fade" id="pills-dinner" role="tabpanel" aria-labelledby="pills-dinner-tab">

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Grilled Top Sirlion Steak</a></h3>
        <p>Spinach and artichokes in a creamy cheese dip with warm tortilla chips &amp; salsa.</p>
      </div>
      <div class="price order-2">
        <strong>$18.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Steak Oscar</a></h3>
        <p>Crisp tortilla and plantain chips covered with lightly spiced ground beef, melted cheese, pickled jalapeños, guacamole, sour cream and salsa.</p>
      </div>
      <div class="price order-2">
        <strong>$23.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Skirt Steak Churrasco</a></h3>
        <p>A heaping mountain of rings, handmade with Panko breading and shredded coconut flakes.</p>
      </div>
      <div class="price order-2">
        <strong>$20.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

    <div class="d-block d-md-flex menu-food-item">
      <div class="text order-1 mb-3">
        <h3><a href="#">Grilled Beef Steak</a></h3>
        <p>Lobster and tender shrimp, with onions, sweet peppers, spinach and our three cheese blend. Griddled and served with tomato salsa and sour cream.</p>
      </div>
      <div class="price order-2">
        <strong>$20.99</strong>
      </div>
    </div> <!-- .menu-food-item -->

  </div>
</div>
<!-- 改成 -->
<div class="tab-content" id="pills-tabContent">
  {% for category in categories %}
  <div class="tab-pane fade show" id="{{category}}" role="tabpanel"
    aria-labelledby="{{category}}-tab">
    {% for meal in meal_list %}
      {% if meal.category == category %}
        <div class="d-block d-md-flex menu-food-item">
          <div class="text order-1 mb-3">
            <h3><a href="{% url 'meals:meal_detail' meal.slug %}">{{meal.name}}</a></h3>
            <p>{{meal.description}}</p>
          </div>
          <div class="price order-2">
            <strong>${{meal.price}}</strong>
          </div>
        </div> <!-- .menu-food-item -->
      {% endif %}
    {% endfor %}
  </div>
  {% endfor %}
</div>

```
## Django页面生成步骤
1. 新建app
`python manage.py startapp reservation`
2. 新建模板
reservation 》template 》Reservation 》reservation.html
3. 建立数据库模型
```python
# models.py
```
4. settings.py添加reservation
5. admin.py绑定模型
6. 更新数据库
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
7. 视图更新
```python
# views.py
from .models import Reservation
from django.shortcuts import render

from reservation.models import Reservation

# Create your views here.
def reserve_table(request):
  context = {}
  return render(request, 'Reservation/reservation.html', context)

```
8. 新建urls.py路由
```python
# urls.py
from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.reserve_table, name='reserve_table')
]

```
9. 项目总urls.py路由添加
```python
# project >> urls.py
urlpatterns = [
    # 省略
    path('reserve_table/', include('reservation.urls', namespace='reservation')),
]
```
10. 表单
```python
# form.py
from django import forms
from .models import Reservation


class ReserveTableForm(forms.ModelForm):
  class Meta:
    model = Reservation
    fields = '__all__'

```
11. 页面制作
```html
<!-- reservation.html -->

```
12. 页面视图
```python
# views.py
# 省略
# Create your views here.
def reserve_table(request):
  reserve_form = ReserveTableForm()
  if request.method == 'POST':
    reserve_form = ReserveTableForm(request.POST)
    if reserve_form.is_valid():
      reserve_form.save()

  context = {'form': reserve_form}
  return render(request, 'Reservation/reservation.html', context)

```
13. 更新原始html导航
```html
<!-- base.html -->
<li><a href="reservation.html">Reserve A Table</a></li>
<!-- 改成 -->
<li><a href="{% url 'reservation:reserve_table' %}">Reserve A Table</a></li>
```

## blog 博客页面
1. 新建app
`python manage.py startapp blog`
2. settings.py添加blog
```python
# settings.py
INSTALLED_APPS = [
    # 省略
    'blog'
]
```
3. 新建模型
```python
# models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  #tags
  category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
  created = models.DateTimeField(default=timezone.now)

class Category(models.Model):
  category_name = models.CharField(max_length=50)

```
4. 更新数据库
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
5. 后台添加
```python
# admin.py
from django.contrib import admin
from .models import Category, Post
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
```
6. 调整模型
```python
# models.py
# 省略

class Post(models.Model):
  # 省略

  class Meta:
    verbose_name = 'post'
    verbose_name_plural = 'posts'

  # 当使用print输出对象的时候，只要自己定义了__str__(self)方法，那么就会打印从在这个方法中return的数据
  def __str__(self):
    return self.title

class Category(models.Model):
  # 省略

  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'

  def __str__(self):
    return self.category_name

```
7. 视图
```python
# views.py
from django.shortcuts import render

# Create your views here.

def post_list(request):
  pass

def post_detail(request,id):
  pass
```
8. 路由
```python
# blog >> urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>', views.post_detail, name='post_detail')
]

```
9. 总路由添加
```python
# project >> urls.py
urlpatterns = [
    # 省略
    path('blog/', include('blog.urls', namespace='blog')),
    path('reserve_table/', include('reservation.urls', namespace='reservation')),
]
```
10. 更新视图
```python
# views.py
from django.shortcuts import render
from .models import Post, Category
# Create your views here.

def post_list(request):
  post_list = Post.objects.all()

  context = {
    'post_list': post_list
  }

  return render(request, 'Post/post_list.html', context)

def post_detail(request,id):
  post_detail = Post.objects.get(id=id)

  context = {
      'post_detail': post_detail
  }

  return render(request, 'Post/post_detail.html', context)

```
11. 新建页面模板
> blog >> templates >> Post >> post_list.html 、post_detail.html
```html
<!-- 头尾直接载入 -->
{% extends 'base.html' %}
{% load static %}
{% block body %}
<!-- 中间部分保留 -->
<div class="main-wrap">
  <!-- 省略 -->
</div>
{% endblock body %}
```
12. 循环数据更新
```html
<!-- post_list.html -->
<!-- 省略 -->
        <div class="row mb-5">
          {% for post in post_list %}
            <div class="col-md-4">
              <div class="media d-block media-bg-white mb-5" data-aos="fade-up" data-aos-delay="400">
                <figure>
                  <a href="blog-single.html"><img src="{{post.image.url}}" alt="Image placeholder" class="img-fluid"></a>
                </figure>
                <div class="media-body">
                  <h3><a href="{% url 'blog:post_detail' post.id %}">{{post}}</a></h3>
                  <p class="post-meta"><span><span class="fa fa-calendar"></span>{{post.created}}</span></p>
                  <p class="mb-4">{{post.content}}</p>
                  <p><a href="{% url 'blog:post_detail' post.id %}"
                      class="btn btn-primary btn-outline-primary btn-sm">Read More</a></p>
                </div>
              </div> <!-- .media -->
            </div>
          {% endfor %}
        </div>
```
```python
# image.url 通过models.py添加
class Post(models.Model):
# 省略
  image = models.ImageField(upload_to='blog/', blank=True, null=True)
# 更新数据库
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
```html
<!-- post_detail.html -->
<!-- 省略 -->
<div class="col-md-7 text-center" data-aos="fade-up">
  <h2 class="heading mb-4">{{post_detail}}</h2>

  <div class="post-info">
    <div class="date-info">{{post_detail.created}}</div>
    <div class="category-info">
      <span class="seperator">|</span>In
      <a href="#" data-title="View all posts in Lifestyle" title="View all posts in Lifestyle">{{post_detail.category}}</a>
    </div>
    <div class="author-info"><span class="seperator">|</span>By <a href="#">{{post_detail.author}}</a></div>
  </div>

</div>
<div class="col-md-8">
  <p>{{post_detail.content}}</p>
  <!-- 省略 -->
</div>
```
13. 页面调整
> post_detail.html
* 去掉多余评论
* 去掉作者简介
* 去掉多余段落
```python
# views.py
  post_detail = Post.objects.get(id=id)
  categories = Category.objects.all()

  context = {
      'post_detail': post_detail,
      'categories': categories
  }

```
14. 标签
> django-taggit的使用
```
django-taggit 是一个简单易用的 Django 标签 app。把 "taggit" 加到在你项目中的 INSTALLED_APPS 中， 然后为你的 model 增加 TaggableManager 就完工了
```
* 安装
`pip install django-taggit`
* 设置
```python
# project >> settings.py
INSTALLED_APPS = [
    # 省略
    'taggit',
    'meals',
    'reservation',
    'blog'
]
```
* 添加
```python
# blog >> models.py
from taggit.managers import TaggableManager

class Post(models.Model):
  # 省略
  tags = TaggableManager(blank=True)
```
* 更新
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
* 循环
```html
<div class="tag-widget post-tag-container mb-5 mt-5">
  <div class="tagcloud">
    <a href="#" class="tag-cloud-link">Life</a>
    <a href="#" class="tag-cloud-link">Sport</a>
    <a href="#" class="tag-cloud-link">Tech</a>
    <a href="#" class="tag-cloud-link">Travel</a>
  </div>
</div>
<!-- 改成 -->
<div class="tag-widget post-tag-container mb-5 mt-5">
  <div class="tagcloud">
    {% for tag in post_detail.tags.all %}
      <a href="#" class="tag-cloud-link">{{tag.name}}</a>
    {% endfor %}
  </div>
</div>
```

[django-taggit参考文档 —— https://github.com/yangyubo/django-taggit](https://github.com/yangyubo/django-taggit)

15. 过滤
```python
# views.py
def post_by_tag(request, tag):
  post_by_tag = Post.objects.filter(tags__name__in=[tag])
  context = {
    'post_list': post_by_tag
  }
  return render(request, 'Post/post_list.html', context)

def post_by_category(request, category):
  post_by_category = Post.objects.filter(category__category_name=category)
  context = {
      'post_list': post_by_category
  }
  return render(request, 'Post/post_list.html', context)

# urls.py
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:id>', views.post_detail, name='post_detail'),
    path('tags=<slug:tag>', views.post_by_tag, name='post_by_tag'),
    path('category=<slug:category>', views.post_by_category, name='post_by_category')
]

```
```html
<!-- 省略 -->
            <div class="tag-widget post-tag-container mb-5 mt-5">
              <div class="tagcloud">
                {% for tag in post_detail.tags.all %}
                  <a href="{% url 'blog:post_by_tag' tag %}" class="tag-cloud-link">{{tag.name}}</a>
                {% endfor %}
              </div>
            </div>
<!-- 省略 -->
              <div class="categories">
                <h3>Categories</h3>
                {% for category in categories %}
                <li><a href="{% url 'blog:post_by_category' category %}">{{category}}</a></li>
                {% endfor %}
              </div>
```
16. 标签
```python
# views
from taggit.models import Tag
# 省略
def post_detail(request,id):
  post_detail = Post.objects.get(id=id)
  categories = Category.objects.all()
  all_tags = Tag.objects.all()

  context = {
      'post_detail': post_detail,
      'categories': categories,
      'all_tags': all_tags
  }
```
```html
<!-- 修改前 -->
  <div class="tagcloud">
    <a href="#" class="tag-cloud-link">Life</a>
    <a href="#" class="tag-cloud-link">Sport</a>
    <a href="#" class="tag-cloud-link">Tech</a>
    <a href="#" class="tag-cloud-link">Travel</a>
    <a href="#" class="tag-cloud-link">Life</a>
    <a href="#" class="tag-cloud-link">Sport</a>
    <a href="#" class="tag-cloud-link">Tech</a>
    <a href="#" class="tag-cloud-link">Travel</a>
  </div>
<!-- 修改后 -->
  <div class="tagcloud">
    {% for tag in all_tags %}
      <a href="{% url 'blog:post_by_tag' tag %}" class="tag-cloud-link">{{tag}}</a>
    {% endfor %}
  </div>
```

* 关于标签不能使用中文后续调整

## 评论
1. 模型
```python
# models.py
class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  content = models.TextField()
  created = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.post

```
2. 更新
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
3. 后台
```python
# admin
from .models import Category, Post, Comment
# 省略
admin.site.register(Comment)

```
#### 注意：中文报错
```
使用def __str__(self):
解决办法：def __unicode__(self):
```
4. 表单
```python
# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = [
      'content'
    ]

```
5. 视图
```python
# views.py
from .models import Post, Category, Comment
# 省略
def post_detail(request,id):
# 省略
  comments = Comment.objects.filter(post=post_detail)

  context = {
    'post_detail': post_detail,
    'categories': categories,
    'all_tags': all_tags,
    'comments': comments
}
```
6. 页面
```html
<!-- post_detail.html -->
  <ul class="comment-list">
    {% for comment in comments %}
      <li class="comment">
        <div class="vcard bio">
          <img src="img/person_1.jpg" alt="Image placeholder">
        </div>
        <div class="comment-body">
          <h3>{{comment.user}}</h3>
          <div class="meta">{{comment.content}}</div>
          <p>{{comment.content}}</p>
        </div>
      </li>
    {% endfor %}
  </ul>
```
## 表单
1. 视图
```python
# views.py
from .forms import CommentForm
# 省略
def post_detail(request,id):
  # 省略
  comment_form = CommentForm()

  if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.user = request.user
      new_comment.post = post_detail
      new_comment.save()
  else:
    comment_form = CommentForm()

  context = {
      # 省略
      'comment_form': comment_form
  }

```
2. 页面
```html
<!-- post_detail.html -->
<!-- 修改前 -->
<form action="#" class="p-5 bg-light">
  <div class="form-group">
    <label for="name">Name *</label>
    <input type="text" class="form-control" id="name">
  </div>
  <div class="form-group">
    <label for="email">Email *</label>
    <input type="email" class="form-control" id="email">
  </div>
  <div class="form-group">
    <label for="website">Website</label>
    <input type="url" class="form-control" id="website">
  </div>

  <div class="form-group">
    <label for="message">Message</label>
    <textarea name="" id="message" cols="30" rows="10" class="form-control"></textarea>
  </div>
  <div class="form-group">
    <input type="submit" value="Post Comment" class="btn btn-primary">
  </div>
</form>
<!-- 修改后 -->
<form method="POST" class="p-5 bg-light">
  {% csrf_token %}
  {{comment_form}}
  <button type="submit" class="btn btn-primary">评论</button>
</form>
```
## 分页
1. django-pagination的使用
```python
# views.py
from django.core.paginator import Paginator
# 省略
def post_list(request):
  post_list = Post.objects.all()
  paginator = Paginator(post_list, 1)

  page = request.GET.get('page')
  post_list = paginator.get_page(page)
```
2. 页面调整
```html
<!-- post_list.html -->
<!-- 修改前 -->
<ul class="pagination custom-pagination">
  <li class="page-item prev"><a class="page-link" href="#"><i class="fa fa-angle-left"></i></a></li>
  <li class="page-item active"><a class="page-linkx href=" #">1</a></li>
  <li class="page-item"><a class="page-link" href="#">2</a></li>
  <li class="page-item"><a class="page-link" href="#">3</a></li>
  <li class="page-item next"><a class="page-link" href="#"><i class="fa fa-angle-right"></i></a></li>
</ul>
<!-- 修改后 -->
<!-- 直接根据文档修改 -->
<div class="pagination">
  <span class="step-links">
    {% if post_list.has_previous %}
    <a href="?page=1">&laquo; first</a>
    <a href="?page={{ post_list.previous_page_number }}">previous</a>
    {% endif %}

    <span class="current">
      Page {{ post_list.number }} of {{ post_list.paginator.num_pages }}.
    </span>

    {% if post_list.has_next %}
    <a href="?page={{ post_list.next_page_number }}">next</a>
    <a href="?page={{ post_list.paginator.num_pages }}">last &raquo;</a>
    {% endif %}
  </span>
</div>
<!-- 原有基础上修改 -->
<div class="row">
  {% if post_list.has_other_pages %}
  <div class="col-md-12">
    <ul class="pagination custom-pagination">
      {% if post_list.has_previous %}
      <li class="page-item prev">
        <a class="page-link" href="?page={{post_list.previous_page_number}}">
          <i class="fa fa-angle-left"></i>
        </a>
      </li>
      {% else %}
        <li class="disabled"></li>
      {% endif %}

      {% for pages in post_list.paginator.page_range %}
        {% if post_list.number == pages %}
          <li class="page-item active"><a class="page-linkx" href="#">{{pages}}</a></li>
        {% else %}
          <li class="page-item active"><a class="page-linkx" href="?page={{pages}}">{{pages}}</a></li>
        {% endif %}
      {% endfor %}
      {% if post_list.has_next %}
        <li class="page-item next">
          <a class="page-link" href="?page={{post_list.next_page_number}}">
            <i class="fa fa-angle-right"></i>
          </a>
        </li>
      {% else %}
        <li class="disabled"></li>
      {% endif %}
    </ul>
  </div>
  {% endif %}
</div>
```

[参考文档：https://docs.djangoproject.com/zh-hans/2.2/topics/pagination/](https://docs.djangoproject.com/zh-hans/2.2/topics/pagination/)

## 关于我们页面
1. 新建
`python manage.py startapp aboutus`
2. 添加
```python
# project >> settings.py
INSTALLED_APPS = [
    # 省略
    'aboutus'
]
```
3. 模型
```python
# aboutus >> models.py
from django.db import models

# Create your models here.
# 简介部分
class AboutUs(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()
  image = models.ImageField(upload_to='about_us/')

  class Meta:
    verbose_name = 'about us '
    verbose_name_plural = 'about us '

  def __str__(self):
    return self.title

# 我们的优势
class Why_Choose_Us(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()

  class Meta:
    verbose_name = 'why choose us '
    verbose_name_plural = 'why choose us '

  def __str__(self):
    return self.title

# 主厨介绍
class Chef(models.Model):
  name = models.CharField(max_length=50)
  title = models.CharField(max_length=50)
  # biography 个人经历
  bio = models.TextField()
  image = models.ImageField(upload_to='chef/')

  class Meta:
    verbose_name = 'chef'
    verbose_name_plural = 'chef'

  def __str__(self):
    return self.name

```
4. 数据
```
python manage.py makemigrations
python manage.py migrate
```
5. 后台
```python
# aboutus >> admin.py
from django.contrib import admin

# Register your models here.
from .models import AboutUs, Why_Choose_Us, Chef

admin.site.register(AboutUs)
admin.site.register(Why_Choose_Us)
admin.site.register(Chef)

```
6. 内容
> 在admin后台添加相关内容：简介、优势、主厨（标题、文字、图片等等）
7. 模板
* 新建templates文件夹 >> aboutus文件夹，添加about.html
8. 视图
```python
# aboutus >> views.py
from django.shortcuts import render
from .models import AboutUs, Why_Choose_Us, Chef
# Create your views here.

def aboutus_list(request):
  pass

```
9. 路由
* 新建urls.py
```python
# aboutus >> urls.py
from django.urls import path
from . import views

app_name = 'aboutus'

urlpatterns = [
    path('', views.aboutus_list, name='aboutus_list')
]
# project >> urls.py
urlpatterns = [
    # 省略
    path('about-us/', include('aboutus.urls', namespace='aboutus')),
    path('reserve_table/', include('reservation.urls', namespace='reservation')),
]
```
10. 渲染
```python
# aboutus >> views.py
# 省略
def aboutus_list(request):
  # objects.last() 返回最后一条数据
  about = AboutUs.objects.last()
  # why_choose_us = Why_Choose_Us.objects.last()
  # chef = Chef.objects.last()
  why_choose_us = Why_Choose_Us.objects.all()
  chef = Chef.objects.all()


  context = {
      'about': about,
      'why_choose_us': why_choose_us,
      'chef': chef
  }

  return render(request, 'aboutus/about.html', context)

```

[django中常用的数据查询方法](https://blog.csdn.net/chen1042246612/article/details/84071006)

11. 预览
* 打开浏览器输入网址：http://localhost:8000/about-us/

12. 页面
```html
<!-- about.html -->
  <div class="section">
    <div class="container">
      <div class="row">
        <div class="col-md-7" data-aos="fade-up">
          <img src="{{about.image.url}}" alt="Image placeholder" class="img-fluid">
        </div>
        <div class="col-md-5 pl-md-5" data-aos="fade-up" data-aos-delay="200">
          <h2 class="mb-4">{{about.title}}</h2>
          <p>{{about.content}}</p>
        </div>
      </div>
    </div>
  </div> <!-- .section -->

<!-- 修改前 -->
  <div class="accordion-item">
    <h3 class="mb-0">
      <a class="btn-block p-3" data-toggle="collapse" href="#collapseOne" role="button"
        aria-expanded="true" aria-controls="collapseOne">Quality Cuisine <span class="icon"></span></a>
    </h3>
    <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
      <div class="p-3">
        <p></p>
      </div>
    </div>
  </div> <!-- .accordion-item -->
<!-- 修改后 -->
  {% for info in why_choose_us %}
    <div class="accordion-item">
      <h3 class="mb-0">
        <a class="btn-block p-3" data-toggle="collapse" href="#collapse{{info.id}}" role="button"
          aria-expanded="true" aria-controls="collapse{{info.id}}">{{info.title}}<span class="icon"></span></a>
      </h3>
      <div id="collapse{{info.id}}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
        <div class="p-3">
          <p>{{info.content}}</p>
        </div>
      </div>
    </div> <!-- .accordion-item -->
  {% endfor %}
<!-- 修改前 -->
  <div class="col-md-3" data-aos="fade-up" data-aos-delay="100">
    <img src="img/person_1.jpg" alt="Image placeholder" class="img-fluid mb-4 rounded">
    <h3 class="mb-3">James Smith</h3>
    <p class="post-meta text-muted">Chef Cook</p>
    <p class="mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laborum cumque velit labore
      placeat corporis ad quisquam odio inventore beatae repudiandae ea quidem saepe doloribus libero, alias,
      eveniet quam at aperiam.</p>
  </div>
  <div class="col-md-3" data-aos="fade-up" data-aos-delay="200">
    <img src="img/person_2.jpg" alt="Image placeholder" class="img-fluid mb-4 rounded">
    <h3 class="mb-3">Rob Woodstone</h3>
    <p class="post-meta text-muted">Chef Cook</p>
    <p class="mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laborum cumque velit labore
      placeat corporis ad quisquam odio inventore beatae repudiandae ea quidem saepe doloribus libero, alias,
      eveniet quam at aperiam.</p>
  </div>
  <div class="col-md-3" data-aos="fade-up" data-aos-delay="300">
    <img src="img/person_3.jpg" alt="Image placeholder" class="img-fluid mb-4 rounded">
    <h3 class="mb-3">Steph Gold</h3>
    <p class="post-meta text-muted">Chef Cook</p>
    <p class="mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laborum cumque velit labore
      placeat corporis ad quisquam odio inventore beatae repudiandae ea quidem saepe doloribus libero, alias,
      eveniet quam at aperiam.</p>
  </div>
  <div class="col-md-3" data-aos="fade-up" data-aos-delay="400">
    <img src="img/person_4.jpg" alt="Image placeholder" class="img-fluid mb-4 rounded">
    <h3 class="mb-3">Jon White</h3>
    <p class="post-meta text-muted">Chef Cook</p>
    <p class="mb-5">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Laborum cumque velit labore
      placeat corporis ad quisquam odio inventore beatae repudiandae ea quidem saepe doloribus libero, alias,
      eveniet quam at aperiam.</p>
  </div>
<!-- 修改后 -->
  {% for one in chef %}
    <div class="col-md-3" data-aos="fade-up" data-aos-delay="100">
      <img src="{{one.image.url}}" alt="Image placeholder" class="img-fluid mb-4 rounded">
      <h3 class="mb-3">{{one.name}}</h3>
      <p class="post-meta text-muted">{{one.title}}</p>
      <p class="mb-5">{{one.bio}}</p>
    </div>
  {% endfor %}
```

## 联系我们 （Contact）
1. 新建
`python manage.py startapp contact`
2. 设置
```python
# project >> settings.py
INSTALLED_APPS = [
    # 省略
    'contact'
]

```
3. 模板
> contact >> templates >> contact >> contact.html
4. 邮件

[https://www.cnblogs.com/AmilyWilly/p/8469880.html](https://www.cnblogs.com/AmilyWilly/p/8469880.html)

```python
# project >> settings.py
# 直接发送邮件到终端
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

```
5. 表单

[http://www.liujiangblog.com/course/django/152](http://www.liujiangblog.com/course/django/152)

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
  name = forms.CharField()
  phone = forms.CharField()
  from_email = forms.EmailField(required = True)
  message = forms.CharField(widget=forms.Textarea, required=True)
```
8. 视图
```python
# views.py
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm
# Create your views here.

def send_email(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      pass
  else:
    form = ContactForm()

  context = {
    'form' : form
  }

  return render(request, 'contact/contact.html', context)

def send_success(request):
  pass
```
9. 路由
```python
# urls.py
from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.send_email, name='send_email'),
    path('success/', views.send_success, name='send_success'),
]

```
10. 页面
```html
{% extends 'base.html' %}
{% load static %}
{% block body %}
  <div class="main-wrap">
    <!-- 省略 -->
      <div class="col-md-10 p-5 form-wrap">
        <form method="POST">
          {% csrf_token %}
          {{form}}
          <div class="col-md-4">
            <button type="submit" class="btn btn-primary">提交</button>
          </div>
        </form>
      </div>
  </div>
{% endblock body %}
```
11. 总路由
```python
# project >> urls.py
urlpatterns = [
    # 省略
    path('contact/', include('contact.urls', namespace='contact')),
```
12. 视图
```python
# views.py
def send_email(request):
  if request.method == 'POST':
    # 省略
    if form.is_valid():
      subject = form.cleaned_data['subject']
      # phone = form.cleaned_data['phone']
      from_email = form.cleaned_data['from_email']
      message = form.cleaned_data['message']

      try:
        send_mail(subject, message, from_email, ['admin@example.com'])
      except BadHeaderError:
        return HttpResponse('ivalid header')

      return redirect('contact:send_success')
```
13. 邮件发送配置
```python
# project >> urls.py
DEFAULT_FROM_EMAIL = 'testing@example.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_PORT = 1025
```

```
SSL/TLS介绍
什么是SSL, 什么是TLS呢？官话说SSL是安全套接层(secure sockets layer)，TLS是SSL的继任者，叫传输层安全(transport layer security)。说白点，就是在明文的上层和TCP层之间加上一层加密，这样就保证上层信息传输的安全。如HTTP协议是明文传输，加上SSL层之后，就有了雅称HTTPS。它存在的唯一目的就是保证上层通讯安全的一套机制。它的发展依次经历了下面几个时期，像手机软件升级一样，每次更新都添加或去除功能，比如引进新的加密算法，修改握手方式等。
```
14. 发送成功返回
```python
# views.py
# 省略
def send_success(request):
  return HttpResponse('thanks you for you email ^-^ ')

```
15. 提交验证

## 搜索
1. 视图
```python
# blog >> views.py
# 省略
from django.db.models import Q
# Create your views here.

def post_list(request):
  post_list = Post.objects.all()

  ## search
  search_query = request.GET.get('q')
  if search_query:
    # __icontains    包含 忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
    post_list = post_list.filter(Q(title__icontains = search_query))

```
2. 页面
```html
<!-- blog >> post_detail.html -->
<!-- method="GET" name="q" value="{{request.Get.q}}" -->
<form action="{% url 'blog:post_list' %}" method="GET" class="search-form">
  <div class="form-group">
    <span class="icon fa fa-search"></span>
    <input type="text" class="form-control" name="q" value="{{request.Get.q}}" placeholder="Type a keyword and hit enter">
  </div>
</form>
```
3. 筛选
```python
# blog >> views.py
  post_list = post_list.filter(
      Q(title__icontains=search_query) |
      Q(content__icontains=search_query) |
      Q(tags__name__icontains=search_query)
  ).distinct()
```

## 首页
1. 新建应用
`python manage.py startapp home`
2. 新建模板
> home >> templates >> home >> index.html
3. 添加应用
```python
# project >> settings.py
INSTALLED_APPS = [
    # 省略
    'home'
]
```
4. 设置路由
```python
# home >> urls.py
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
]

```
5. 添加视图
```python
# home >> views.py

```
6. 总路由
```python
# project >> urls.py
urlpatterns = [
    # 省略
    path('', include('home.urls', namespace='home')),
]
```
7. 页面
```html
<!-- home >> index.html -->
{% extends 'base.html' %}
{% load static %}
{% block body %}
  <div class="main-wrap">
    <!-- 省略 -->
  </div>
{% endblock body %}
```
8. 后台数据添加
9. 视图调整
```python
# home >> views.py
from django.shortcuts import render
from meals.models import Meals
# Create your views here.

def home(request):

  context = {
    'meals': meals
  }

  return render(request, 'home/index.html', context)

```
10. 页面循环遍历
```html
<!-- home >> templates >> home >> index.html -->
<div class="menus d-flex bg-light">
  {% for meal in meals %}
    <div class="d-flex item">
      <div class="image" style="background-image: url({{meal.image.url}});" data-aos="fade"></div>
      <div class="text">
        <h3>{{meal.name}}</h3>
        <p>{{meal.description}}</p>
        <p class="price">${{meal.price}}</p>
      </div>
    </div> <!-- .item -->
  {% endfor %}
</div>
```
11. 调整视图
```python
# home >> views.py
from django.shortcuts import render
from meals.models import Meals, Category
# Create your views here.

def home(request):
  meals = Meals.objects.all();
  meal_list = Meals.objects.all();
  categories = Category.objects.all();

  context = {
    'meals': meals,
    'meal_list': meal_list,
    'categories': categories
  }

  return render(request, 'home/index.html', context)

```
12. 更新页面
```html
<!-- 切换 -->
  <div class="section">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8" data-aos="fade-up">

          <h2 class="mb-5 text-center">Menu List with Price</h2>

          <ul class="nav site-tab-nav" id="pills-tab" role="tablist">
            {% for category in categories %}
            <li class="nav-item">
              <a class="nav-link " id="{{category}}-tab" data-toggle="pill" href="#{{category}}" role="tab"
                aria-controls="{{category}}" aria-selected="true">{{category}}</a>
            </li>
            {% endfor %}
          </ul>

          <div class="tab-content" id="pills-tabContent">
            {% for category in categories %}
            <div class="tab-pane fade show" id="{{category}}" role="tabpanel" aria-labelledby="{{category}}-tab">
              {% for meal in meal_list %}
              {% if meal.category == category %}
              <div class="d-block d-md-flex menu-food-item">
                <div class="text order-1 mb-3">
                  <h3><a href="{% url 'meals:meal_detail' meal.slug %}">{{meal.name}}</a></h3>
                  <p>{{meal.description}}</p>
                </div>
                <div class="price order-2">
                  <strong>${{meal.price}}</strong>
                </div>
              </div> <!-- .menu-food-item -->
              {% endif %}
              {% endfor %}
            </div>
            {% endfor %}
          </div>

        </div>
      </div>
    </div>
  </div>

```

13. 视图更新
```python
# home >> views.py
# 省略
from blog.models import Post

# Create your views here.

def home(request):
  # 省略
  posts = Post.objects.all()
  latest_post = Post.objects.last()


  context = {
    # 省略
    'posts': posts,
    'latest_post': latest_post,
  }

  return render(request, 'home/index.html', context)

```
14. 页面添加blog部分
```html
<div class="row">
  <div class="col-lg-6">
    {% for post in posts %}
      <div class="media d-block d-lg-flex mb-5"  data-aos="fade-up" data-aos-delay="100">
        <figure class="mr-4 horizontal">
          <img src="{{post.image.url}}" alt="Image placeholder" class="img-fluid">
        </figure>
        <div class="media-body">
          <h3><a href="#">{{post.title}}</a></h3>
          <p class="post-meta"><span><span class="fa fa-calendar"></span>{{post.created}}</span></p>
          <p>{{post.content}}</p>
          <p><a href="#" class="btn btn-primary btn-outline-primary btn-sm">Read More</a></p>
        </div>
      </div> <!-- .media -->
    {% endfor %}
  </div> <!-- .col-md-6 -->

  <div class="col-lg-6">
    <div class="media d-block mb-5" data-aos="fade-up"  data-aos-delay="400">
      <figure>
        <a href="#"><img src="{{latest_post.image.url}}" alt="Image placeholder" class="img-fluid"></a>
      </figure>
      <div class="media-body">
        <h3><a href="#">{{latest_post.title}}</a></h3>
        <p class="post-meta"><span><span class="fa fa-calendar"></span>{{latest_post.created}}</span></p>
        <p>{{latest_post.content}}</p>
        <p><a href="#" class="btn btn-primary btn-outline-primary btn-sm">Read More</a></p>
      </div>
    </div> <!-- .media -->
  </div>
</div>
```

15. 视图添加
```python
# home >> views.py
# 省略
from aboutus.models import Why_Choose_Us
# Create your views here.

def home(request):
  # 省略
  why_choose_us = Why_Choose_Us.objects.all()

  context = {
    # 省略
    'why_choose_us': why_choose_us
  }

  return render(request, 'home/index.html', context)

```
16. 页面（选择我们部分）更新
```html
<!-- 选择我们的理由 -->
<!-- 直接复制 -->
```

## 页面优化
1. 文字限定
```html
<!-- home >> index.html -->
<p>{{meal.description|truncatewords:20}}</p>
<!-- 只对英文单词有效 -->
```
2. 导航调整
```html
<!-- base.html -->
<!-- 修改前 -->
<nav class="site-menu">
  <div class="site-menu-inner">
    <ul class="list-unstyled">
      <li class="active"><a href="index.html">Home</a></li>
      <li><a href="about.html">About Us</a></li>
      <li><a href="menu.html">Our Menu</a></li>
      <li><a href="blog.html">Our Blog</a></li>
      <li><a href="{% url 'reservation:reserve_table' %}">Reserve A Table</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
  </div>
</nav>
<!-- 修改后 -->
<nav class="site-menu">
  <div class="site-menu-inner">
    <ul class="list-unstyled">
      <li class="active"><a href="/">Home</a></li>
      <li><a href="{% url 'aboutus:aboutus_list' %}">About Us</a></li>
      <li><a href="{% url 'blog:post_list' %}">Our Blog</a></li>
      <li><a href="{% url 'reservation:reserve_table' %}">Reserve A Table</a></li>
      <li><a href="{% url 'contact:send_email' %}">Contact</a></li>
    </ul>
  </div>
</nav>
```
3. bootstrap4

[参考文档：https://github.com/zostera/django-bootstrap4](https://github.com/zostera/django-bootstrap4)

* 安装
`pip install django-bootstrap4`
* 设置
```python
# project >> settings.py
INSTALLED_APPS = [
    # 省略
    'bootstrap4',
    'meals',
```
* 替换
```html
<!-- blog >> templates >> Post >> post_detail.html -->
<!-- 修改前 -->
{{comment_form}}
<button type="submit" class="btn btn-primary">评论</button>

<!-- 修改后 -->
{% bootstrap_form comment_form %}
{% buttons %}
    <button type="submit" class="btn btn-primary">评论</button>
{% endbuttons %}

<!-- contact.html -->
<!-- 修改前 -->
{{form}}
<div class="col-md-4">
  <button type="submit" class="btn btn-primary">提交</button>
</div>
<!-- 修改后 -->
{% bootstrap_form form %}
{% buttons %}
    <button type="submit" class="btn btn-primary">提交</button>
{% endbuttons %}
```
4. django-summernote 富文本编辑器的使用

[参考文档：https://github.com/summernote/django-summernote](https://github.com/summernote/django-summernote)

* 安装
`pip install django-summernote`
* 设置
```python
# project >> settings.py
INSTALLED_APPS = [
  # 省略
  'bootstrap4',
  'django-summernote',
```
* 路由
```python
# project >> urls.py
urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
```
* 数据
`python manage.py migrate`
* 后台
```python
# meals >> admin.py
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import Meals, Category

# Apply summernote to all TextField in model.
class MealsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'

admin.site.register(Meals, MealsAdmin)
admin.site.register(Category)

# 同样，修改blog >> admin.py
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Post, Comment
# Register your models here.

# Apply summernote to all TextField in model.
class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)

```

## 后台设置
1. 整体设置
```python
# project >> urls.py
# 后台管理标题设置
# admin.site.site_header = "Resturant AdminPanel"
# admin.site.site_title = "Resturant App Admin"
# admin.site.site_index_title = "Welcome To Resturant Admin Panel"
admin.site.site_header = "餐馆后台管理系统"
admin.site.site_title = "餐馆管理后台"
admin.site.site_index_title = "欢迎使用餐馆后台管理系统"
```
2. 博客后台
```python
# blog >> admin.py
# 省略
class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'
  list_display = ['title','author','category','created']
  search_fields = ['title','content']
  list_filter = ['category','tags']

```
3. 菜单后台
```python
# meals >> admin.py
# 省略
class MealsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'
  list_display = ['name', 'preperation_time', 'people', 'price']
  search_fields = ['name', 'description']
  list_filter = ['category', 'people']

```

## python django 数据库查询
```
__exact        精确等于 like 'aaa'
__iexact    精确等于 忽略大小写 ilike 'aaa'
__contains    包含 like '%aaa%'
__icontains    包含 忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
__gt    大于
__gte    大于等于
__lt    小于
__lte    小于等于
__in     存在于一个list范围内
__startswith   以...开头
__istartswith   以...开头 忽略大小写
__endswith     以...结尾
__iendswith    以...结尾，忽略大小写
__range    在...范围内
__year       日期字段的年份
__month    日期字段的月份
__day        日期字段的日
__isnull=True/False
__isnull=True 与 __exact=None的区别
```

## request.POST.get('key') 、 request.GET.get('key', '')
```
request.POST是用来接受从前端表单中传过来的数据，比如用户登录过程中传递过来的username、passwrod等字段。返回类型是字典；

在后台进行数据获取时，有两种方法（以username为例）：request.POST['username']与request.POST.get('username')，那么这两者有什么不同之处呢？

如果传递过来的数值不为空，那么这两种方法都没有错误，可以得到相同的结果。但是如果传递过来的数值为空，那么request.POST['username']则会提示Keyerror错误，而request.POST.get('username')则不会报错，而是返回一个None。
```

## 关于django views视图函数
* 一. 创建views.py文件，在工程文件夹根目录创建views.py视图文件，其实任意文件名都可以，使用views是为了遵循传统。
* 二. HttpResponse函数
* 三．调用render函数返回一个网页
```
参数详解：

request: 是一个固定参数, 就是指通过接受到的通过wsgi处理过的客户端浏览器请求数

据。

template_name:templates中定义的HTML文件, 要注意路径比如'templates\polls\index.html', 参数就要写'polls\index.html'

context: 要传入上下文中用于渲染呈现的数据, 默认是一个字典格式，键即下文html模板中需要被替换的元素，键值即在views视图函数中需要传到html模板中变量需要替换成的值。

content_type: 生成的文档要使用的MIME 类型。默认为DEFAULT_CONTENT_TYPE 设置的值。

status: http的响应代码,默认是200.

using: 用于加载模板使用的模板引擎的名称。
```

[django views视图函数](https://www.cnblogs.com/fengjunhua/p/7813317.html)


## Django常见错误总结: 细数我们一起走过的大坑
[https://blog.csdn.net/weixin_42134789/article/details/82184481](https://blog.csdn.net/weixin_42134789/article/details/82184481)

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