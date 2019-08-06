from django.db import models
# Create your models here.
# 创建产品分类表
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)
# 创建产品信息表
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    weight = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

# from django.db import models

# # Create your models here.
# class Product(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     type = models.CharField(max_length=20)
