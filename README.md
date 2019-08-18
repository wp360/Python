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