from django.db import models
# Create your models here.
# 创建产品分类表
# class Type(models.Model):
#     id = models.AutoField(primary_key=True)
#     type_name = models.CharField(max_length=20)
# # 设置返回值，若不设置，则默认返回Type对象
# def __str__(self):
#     return self.type_name

# 设置字段中文名，用于admin后台显示
class Type(models.Model):
    id = models.AutoField('序号', primary_key=True)
    type_name = models.CharField('产品类型', max_length=20)
    # 设置返回值
    def __str__(self):
        return self.type_name

# 创建产品信息表
# class Product(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50)
#     weight = models.CharField(max_length=20)
#     size = models.CharField(max_length=20)
#     type = models.ForeignKey(Type, on_delete=models.CASCADE)

# 设置字段中文名，用于admin后台显示
class Product(models.Model):
    id = models.AutoField('序号', primary_key=True)
    name = models.CharField('名称',max_length=50)
    weight = models.CharField('重量',max_length=20)
    size = models.CharField('尺寸',max_length=20)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,verbose_name='产品类型')
    # 设置返回值
    def __str__(self):
        return self.name
# from django.db import models

# # Create your models here.
# class Product(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     type = models.CharField(max_length=20)
