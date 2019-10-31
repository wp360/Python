"""demo2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#引入视图类
from app01.views import Type1View,Type2View,Type3View,Type4View
# 引入类别总类视图
from app01.views import TypeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/type1/',Type1View.as_view()),
    path('api/type2/',Type2View.as_view()),
    path('api/type3/',Type3View.as_view()),
    path('api/type4/',Type4View.as_view()),
    path('api/type/',TypeView.as_view())
]