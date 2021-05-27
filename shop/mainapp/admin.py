from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    ''' Категории в Админке '''

    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):

    ''' Ноутбуки в Админке '''

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='noutbuk'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):

    ''' Смартфоны в в Админке '''

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartfony'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
