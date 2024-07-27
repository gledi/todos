from django.views.generic import ListView, DetailView

from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
