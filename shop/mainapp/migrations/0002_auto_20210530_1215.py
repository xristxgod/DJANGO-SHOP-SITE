# Generated by Django 3.2.3 on 2021-05-30 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='cartproduct',
            options={'verbose_name': 'Корзина товара', 'verbose_name_plural': 'Корзина товаров'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Кастомайзер', 'verbose_name_plural': 'Кастомайзеры'},
        ),
        migrations.AlterModelOptions(
            name='notebook',
            options={'verbose_name': 'Ноутбук', 'verbose_name_plural': 'Ноутбуки'},
        ),
        migrations.AlterModelOptions(
            name='smartphone',
            options={'verbose_name': 'Смартфон', 'verbose_name_plural': 'Смартфоны'},
        ),
        migrations.AddField(
            model_name='cart',
            name='for_anonymous_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='accum_volum',
            field=models.CharField(max_length=255, verbose_name='Обьем ботареи'),
        ),
    ]