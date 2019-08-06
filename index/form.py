from django import forms
from .models import *

# 表单
# enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

class ProductForm(forms.Form):
    name = forms.CharField(max_length=20, label='名字',)
    weight = forms.CharField(max_length=50, label='重量')
    size = forms.CharField(max_length=50, label='尺寸')
    choices_list = [(i+1, v['type_name']) for i,v in enumerate(Type.objects.values('type_name'))]
    type = forms.ChoiceField(choices=choices_list, label='产品类型')
