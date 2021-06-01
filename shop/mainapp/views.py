from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, View
from django.http import HttpResponseRedirect

from .models import *

class BaseView(View):

    ''' Показать гланую страницу '''

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'customer': customer,
            'cart': cart,
            'categories': categories
        }
        return render(request, 'base.html', context)

def get_all_products(request):

    ''' Вывод всех товров из магазина '''

    products = LatestProduct.objects.get_products_for_main_page(
        'notebook',
        'smartphone',
        with_respect_to='notebook'
    )
    context = {'products': products}
    return render(request, 'all_products.html', context)

class ProductDetailView(DetailView):

    ''' Вывод отедльной категории товаров '''

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone

    }

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context

class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

class AddToCartView(View):

    ''' Добовление товара в корзину '''

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart.owner,
            cart=cart,
            content_type=content_type,
            object_id=product.id,
            final_price=product.price,
        )
        cart.products.add(cart_product)
        return HttpResponseRedirect('/cart/')


class CartView(View):

    ''' Корзина '''

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        context = {
            'cart': cart,
        }
        return render(request, 'cart.html', context)


