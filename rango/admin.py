from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')
    

class PageInline(admin.StackedInline):
    model = Page
    
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PageInline] 
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

