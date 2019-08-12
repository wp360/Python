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