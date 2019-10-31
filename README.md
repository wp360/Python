## 项目构建
1. 打开cmd输入指令（前提已经安装python、django、django-admin等）
`django-admin startproject demo2`
2. 新建应用app01（切换到demo2文件夹下 cd demo2）
`python manage.py startapp app01`
3. 安装相关依赖包
`pip install djangorestframework markdown Django-filter pillow django-guardian coreapi`
4. settings.py设置
```python
INSTALLED_APPS = [
    # ...
    # 省略
    'app01.apps.App01Config',
    'rest_framework'
]
```
5. 新建类别表
```python
# models.py
from django.db import models
from datetime import datetime
# Create your models here.

"""
一级类目
"""
class Type1(models.Model):
    name = models.CharField(max_length=10,default="",verbose_name="类目名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

"""
二级类目
"""
class Type2(models.Model):
    parent = models.ForeignKey(Type1,verbose_name="父级类别",null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=10,default="",verbose_name="类目名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name = '商品类别2'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

"""
三级类目
"""
class Type3(models.Model):
    parent = models.ForeignKey(Type2,verbose_name="父级类别",null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=10,default="",verbose_name="类目名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name = '商品类别3'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

"""
四级类目
"""
class Type4(models.Model):
    parent = models.ForeignKey(Type3,verbose_name="父级类别",null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=10,default="",verbose_name="类目名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name = '商品类别4'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

```
6. 数据更新
```
python manage.py makemigrations
python manage.py migrate
```
7. 设置中文
```python
# settings.py
LANGUAGE_CODE = 'zh-hans' #en-us

TIME_ZONE = 'Asia/Shanghai' #UTC
```
8. 后台数据模型注册
```python
# admin.py
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Type1)
admin.site.register(Type2)
admin.site.register(Type3)
admin.site.register(Type4)
```
9. 启动项目
`python manage.py runserver`
10. 添加数据
11. 解决跨域问题
* 安装插件
`pip install Django-cors-headers`
* settings配置
```python
INSTALLED_APPS = [
    # 省略
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # 省略
]

# 解决跨域
CORS_ORIGIN_ALLOW_ALL = True
```

## 四表合一
* 新建Type类
* 数据导入
* 序列化
```python
# serializers.py
from .models import Type
class TypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Type
        fields="__all__"

```
* 创建视图类
```python
# views.py
from .models import Type
#导入序列化类
from .serializers import TypeModelSerializer
class TypeView(APIView):
    """
    操作类别表
    """
    renderer_classes = [JSONRenderer]
    def get(self,request,format=None):
        types=Type.objects.all()
        types_serializer = TypeModelSerializer(types, many=True)
        return Response(types_serializer.data)
        def post(self,request):
        name=request.data.get('name')
        category_type=request.data.get('lei')
        parent_category_id=request.data.get('parent')
        type=Type()
        type.name=name
        type.category_type=category_type
        if parent_category_id:
            parent_category=Type.objects.filter(id=parent_category_id).first()
            type.parent_category=parent_category
        type.save()
        type_serializer=TypeModelSerializer(type)
        return Response(type_serializer.data)

```
* 路由
```python
# urls.py
from app01.views import TypeView
urlpatterns = [
    #......
    path('api/type/',TypeView.as_view())
]

```
* 使用POSTMAN添加数据
```
输入连接： http://127.0.0.1:8000/api/type/
采用POST方法
form-data添加参数
```
* 修改前端调用api的js部分
```js
<script>
import Axios from 'axios';
export default {
  name: 'app',
  data () {
    return {
      type:[],
      one:[],
      two:[],
      flag:false,
      three1:[],
      four1:[]
    }
  },
  methods: {
    getData(){
      const api='http://127.0.0.1:8000/api/type/';
      var _this=this
      
      Axios.get(api)
      .then(function (response) {
        _this.type=response.data;
        for(var i=0;i<_this.type.length;i++){
          if(_this.type[i].category_type===1){
            _this.one.push(_this.type[i])
          } 
        }
        for(var j=0;j<_this.type.length;j++){
          if(_this.type[j].category_type===2){
            _this.two.push(_this.type[j])
          } 
        }
      })
      .catch(function (error) {
      console.log(error);
      });
      
    },
    open(index){
      this.three1=[]
      this.four1=[]
      var parent=this.two[index].id
      for(var i=0;i<this.type.length;i++){
        if(this.type[i].parent_category===parent){
          this.three1.push(this.type[i].name)
        }
        if(this.type[i].category_type===4){
          this.four1.push(this.type[i].name)
        }
      }
      this.flag=true
    },
    close(){
      this.flag=false
    }
  },
  mounted() {
    this.getData()
  }
}
</script>

```

* 后台登录：admin、admin123

## Django-guardian实现对象级别的权限控制
> django-guardian是为Django提供额外的基于对象权限的身份验证后端。
[https://blog.csdn.net/bbwangj/article/details/89159727](https://blog.csdn.net/bbwangj/article/details/89159727)