from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import Meals, Category

# Apply summernote to all TextField in model.
class MealsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
  summernote_fields = '__all__'
  list_display = ['name', 'preperation_time', 'people', 'price']
  search_fields = ['name', 'description']
  list_filter = ['category', 'people']

admin.site.register(Meals, MealsAdmin)
admin.site.register(Category)
