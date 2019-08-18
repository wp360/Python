from django.shortcuts import render
from .models import Post, Category
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

  context = {
      'post_detail': post_detail,
      'categories': categories
  }

  return render(request, 'Post/post_detail.html', context)
