from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=50)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='blog/', blank=True, null=True)
  tags = TaggableManager(blank=True)
  category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
  created = models.DateTimeField(default=timezone.now)

  class Meta:
    verbose_name = 'post'
    verbose_name_plural = 'posts'

  # 当使用print输出对象的时候，只要自己定义了__str__(self)方法，那么就会打印从在这个方法中return的数据
  def __str__(self):
    return self.title

class Category(models.Model):
  category_name = models.CharField(max_length=50)

  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'

  def __str__(self):
    return self.category_name

class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  content = models.TextField()
  created = models.DateTimeField(default=timezone.now)

  # def __str__(self):
  #  return str(self.content)
  def __unicode__(self):
    return self.post
