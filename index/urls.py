from django.urls import path, re_path
from . import views
urlpatterns = [
    # 配置简单URL
    path('', views.index),
    # 添加带有字符类型、整型和slug的URL
    # path('<year>/<int:month>/<slug:day>', views.mydate),
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2}).html', views.mydate),
    # 带参数name的URL
    re_path('(?P<year>[0-9]{4}).html', views.myyear, name='myyear'),
    # 参数为字典的URL
    re_path('dict/(?P<year>[0-9]{4}).htm', views.myyear_dict, {'month': '05'}, name='myyear_dict')
]
