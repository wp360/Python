from django.shortcuts import render
from .models import Post, Category, Comment
from taggit.models import Tag
# Create your views here.

def post_list(request):
  post_list = Post.objects.all()

  context = {
    'post_list': post_list
  }

  return render(request, 'Post/post_list.html', context)

def post_detail(request,id):
  post_detail = Post.objects.get(id=id)
  categories = Category.objects.all()
  all_tags = Tag.objects.all()
  comments = Comment.objects.filter(post=post_detail)

  context = {
      'post_detail': post_detail,
      'categories': categories,
      'all_tags': all_tags,
      'comments': comments
  }

  return render(request, 'Post/post_detail.html', context)

def post_by_tag(request, tag):
  post_by_tag = Post.objects.filter(tags__name__in=[tag])
  context = {
    'post_list': post_by_tag
  }
  return render(request, 'Post/post_list.html', context)

def post_by_category(request, category):
  post_by_category = Post.objects.filter(category__category_name=category)
  context = {
      'post_list': post_by_category
  }
  return render(request, 'Post/post_list.html', context)
