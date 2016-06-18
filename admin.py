from django.contrib import admin
from .models import Question, Publication, Article, TimeSlot
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('publications',)


admin.site.register(Question)
admin.site.register(Publication)
admin.site.register(Article, ArticleAdmin)
admin.site.register(TimeSlot)
