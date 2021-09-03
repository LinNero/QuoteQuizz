from django.contrib import admin
from .models import Category, Source, QuestionSet, Quote, Question, UsersQuestions



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']


class QuoteInline(admin.TabularInline):
    model = Quote


class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'category_id']
    list_filter = ['category_id']
    search_fields = ['name']
    inlines = [QuoteInline]


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text', 'source', 'rating']
    list_filter = ['source']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quote_id', 'question_set_id']
    list_filter = ['question_set_id']


class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_id']
    list_filter = ['category_id']


class UsersQuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'is_correct', 'question']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UsersQuestions, UsersQuestionsAdmin)

