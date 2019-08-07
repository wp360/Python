from django.contrib import admin
from .models import *
# Register your models here.

# 方法一
# 将模型直接注册到admin后台
# admin.site.register(Product)

# 方法二
# 自定义ProductAdmin类并继承ModelAdmin
# 注册方法一，使用Python装饰器将ProductAdmin和模型Product绑定注册到后台
# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 设置显示的字段
    list_display = ['id', 'name', 'weight', 'size', 'type',]
# 注册方法二
admin.site.register(Product, ProductAdmin)