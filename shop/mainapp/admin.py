from django.contrib import admin


from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    ''' Категории в Админке '''

    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    ''' Продукты в Админке '''


    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)

