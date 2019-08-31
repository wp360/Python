from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import Meals, Category

# Apply summernote to all TextField in model.
class MealsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'

admin.site.register(Meals, MealsAdmin)
admin.site.register(Category)
