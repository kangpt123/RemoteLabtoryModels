from django.contrib import admin
from .models import Question, Publication, Article
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('publications',)


admin.site.register(Question)
admin.site.register(Publication)
admin.site.register(Article, ArticleAdmin)
