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
