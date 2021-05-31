from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin


from .models import *



class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray'

            })
    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data



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
            return ModelChoiceField(Category.objects.filter(slug='notebook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):

    ''' Смартфоны в в Админке '''

    prepopulated_fields = {'slug': ('title',)}
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
