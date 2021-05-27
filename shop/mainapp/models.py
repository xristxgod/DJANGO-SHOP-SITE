from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


User = get_user_model()

class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filrer(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__.meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProduct:

    objects = LatestProductManager()

class Category(models.Model):

    ''' Категории '''

    name = models.CharField(max_length=150, verbose_name='Имя категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):

    ''' Товар '''

    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание товара', null=True)
    price = models.DecimalField(max_digits=9, verbose_name='Цена', decimal_places=2)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Notebook(Product):

    ''' Характеристика для разделов с ноутбуками '''

    diagonal = models.CharField(max_length=255, verbose_name='Диогональ')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Чистота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккамулятора')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

class Smartphone(Product):

    ''' Характеристика для раздела со смортфонами '''

    diagonal = models.CharField(max_length=255, verbose_name='Диогональ')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolutions = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volum = models.CharField(max_length=255, verbose_name='Обьем ботареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный обьем встраемой памяти')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

class CartProduct(models.Model):

    ''' Корзина товаров '''

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, verbose_name='Общая цена', decimal_places=2)

    def __str__(self):
        return f'Продукты: {self.product.title}'

    class Meta:
        verbose_name = 'Корзина товара'
        verbose_name_plural = 'Корзина товаров'

class Cart(models.Model):

    ''' Корзина '''

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_product = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, verbose_name='Общая цена', decimal_places=2)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class Customer(models.Model):

    ''' Кастомайзер '''

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=28, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'Покупатель: {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Кастомайзер'
        verbose_name_plural = 'Кастомайзеры'



