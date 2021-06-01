from django import template
from django.utils.safestring import mark_safe
from mainapp.models import Smartphone, Category, LatestProduct, CartProduct, Cart, Customer

register = template.Library()

TABLE_HEAD = '''
            <table class="table">
                <tbody>
            '''
TABLE_TAIL = '''
                </tbody>
            </table>
            '''
TABLE_CONTENT = '''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                '''
PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Дисплаей': 'display',
        'Процессор': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работы аккамулятора': 'time_without_charge'
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Дисплаей': 'display',
        'Разрешение экрана': 'resolutions',
        'Заряд аккамулятора хватает на': 'accum_volum',
        'Оперативная память': 'ram',
        'Главная камера': 'main_cam_mp',
        'Фронтальная камера': 'frontal_cam_mp',
        'Наличие SD карты': 'sd',
        'Максимальный обьем SD катры': 'sd_volume_max',
    }

}

def get_product_spec(product, model_name):
    table_content = ''
    for title, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(title, getattr(product, value))

    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    # if isinstance(product, Smartphone):
    #     if not product.sd:
    #         PRODUCT_SPEC['smartphone'].pop('Максимальный обьем SD катры')
    #         # PRODUCT_SPEC['smartphone'].pop('Наличие SD карты')
    #     else:
    #         PRODUCT_SPEC['smartphone']['Максимальный обьем SD катры'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

# @register.inclusion_tag('inc/_nav.html')
# def get_category_and_count():
#     categories = Category.objects.get_categories_for_left_sidebar()
#     return {
#         'categories': categories,
#
#     }
# <!--{% get_category_and_count %}-->