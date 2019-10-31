from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Type1)
admin.site.register(Type2)
admin.site.register(Type3)
admin.site.register(Type4)
# 四表合一
admin.site.register(Type)