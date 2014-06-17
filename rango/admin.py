from django.contrib import admin
from rango.models import Category, Page, UserProfile


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ['name']}),
        ('Statistics', {'fields': ['views', 'likes']}),
    ]
    list_display = ('name', 'views', 'likes')

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'views')
    search_fields = ['title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)