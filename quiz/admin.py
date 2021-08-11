from django.contrib import admin
from .models import Category, Source, QuestionSet, Quote, Question


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']



class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'category_id']
    list_filter = ['category_id']
    search_fields = ['name']


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'source', 'rating']
    list_filter = ['source']




# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(QuestionSet)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Question)

