from django.shortcuts import render
from django.http import HttpResponse
import csv
# 页面渲染
from django.shortcuts import render,redirect
from .models import Product
# 表单
from .form import *

# Create your views here.

def download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'A', 'B', 'C'])
    return response

# def index(request):
#     type_list = Product.objects.values('type').distinct()
#     name_list = Product.objects.values('name','type')
#     context = {'title': '首页', 'type_list': type_list, 'name_list': name_list}
#     return render(request, 'index.html',context=context, status=200)

# locals()使用技巧
def index(request):
    # type_list = Product.objects.values('type').distinct()
    # name_list = Product.objects.values('name','type')
    # title = '首页'
    # return render(request, 'index.html',context=locals(), status=200)
    # 表单
    # product = ProductForm()
    # return render(request, 'data_form.html',locals())
    # GET请求
    if request.method == 'GET':
        product = ProductForm()
        return render(request, 'data_form.html',locals())
    # POST请求
    else:
        product = ProductForm(request.POST)
        if product.is_valid():
            # 获取网页控件name的数据
            # 方法一
            name = product['name']
            # 方法二
            # cleaned_data将控件name的数据进行清洗，转换成Python数据类型
            cname = product.cleaned_data['name']
            return HttpResponse('提交成功')
        else:
            # 将错误信息输出，error_msg是将错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())
            
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # 相对路径，代表首页地址
        return redirect('/')
        # 绝对路径，完整的地址信息
        # return redirect('http://127.0.0.1:8000/')
    else:
        if request.GET.get('name'):
            name = request.GET.get('name')
        else:
            name = 'Everyone'
        return HttpResponse('username is '+ name)

# 视图函数model_index
def model_index(request, id):
    if request.method == 'GET':
        instance = Product.objects.filter(id=id)
        # 判断数据是否存在
        if instance:
            product = ProductModelForm(instance=instance[0])
        else:
            product = ProductModelForm()
        return render(request, 'data_form.html', locals())
    else:
        product = ProductModelForm(request.POST)
        if product.is_valid():
            # 获取weight的数据，并通过clean_weight进行清洗，转换成Python数据类型
            weight = product.cleaned_data['weight']
            # 直接保存到数据库
            # product.save()
            # save方法设置commit=False，生成数据库对象product_db，然后可对该对象的属性值修改并保存
            product_db = product.save(commit=False)
            product_db.name = '我的iPhone'
            product_db.save()
            # save_m2m()方法是保存ManyToMany的数据模型
            #product.save_m2m()
            return HttpResponse('提交成功!weight清洗后的数据为：'+weight)
        else:
            # 将错误信息输出，error_msg是将错误信息以json格式输出
            error_msg = product.errors.as_json()
            print(error_msg)
            return render(request, 'data_form.html', locals())
# 通用视图
from django.views.generic import ListView
class ProductList(ListView):
    # context_object_name设置Html模版的变量名称
    context_object_name = 'type_list'
    # 设定HTML模版
    template_name='index.html'
    # 查询数据
    queryset = Product.objects.values('type').distinct()

    # 重写 get_queryset 方法，对模型product进行数据筛选。
    def get_queryset(self):
        # 获取URL的变量id
        print(self.kwargs['id'])
        # 获取URL的参数name
        print(self.kwargs['name'])
        # 获取请求方式
        print(self.request.method)
        type_list = Product.objects.values('type').distinct()
        return type_list

    # 添加其他变量
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_list'] = Product.objects.values('name','type')
        return context

# 带变量的URL的视图函数
def mydate(request, year, month, day):
    return HttpResponse(str(year) +'/'+ str(month) +'/'+ str(day))
# 参数name的URL的视图函数
def myyear(request, year):
    return render(request, 'myyear.html')
# 参数为字典的URL的视图函数
def myyear_dict(request, year, month):
    return render(request, 'myyear_dict.html',{'month':month})