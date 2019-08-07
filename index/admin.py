from django.contrib import admin
from .models import *
# Register your models here.

# 修改title和header
admin.site.site_title = 'MyDjango后台管理'
admin.site.site_header = 'MyDjango'

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
    # 设置搜索字段，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['id', 'name','type__type_name']
    # 设置过滤器，如有外键应使用双下划线连接两个模型的字段
    list_filter = ['name','type__type_name']
    # 设置排序方式，['id']为升序，降序为['-id']
    ordering = ['id']
    # 设置时间选择器，如字段中有时间格式才可以使用
    # date_hierarchy = Field
    # 在添加新数据时，设置可添加数据的字段
    fields = ['name', 'weight', 'size', 'type']
    # 设置可读字段,在修改或新增数据时使其无法设置
    readonly_fields = ['name']
# 注册方法二
admin.site.register(Product, ProductAdmin)