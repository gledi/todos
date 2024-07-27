import stripe
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


def get_publishable_key(request):
    return JsonResponse({"publishableKey": settings.STRIPE_PUBLISHABLE_KEY})


def create_checkout_session(request, pk):
    product = get_object_or_404(Product, pk=pk)
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + reverse('payment-success', kwargs={'pk': pk}) + "?session_id={{CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + reverse('payment-cancel', kwargs={'pk': pk}),
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price': product.stripe_price_id,
                    'quantity': 1,
                }
            ]
        )
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def get_payment_success(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/payment_success.html', {'product': product})


def get_payment_cancel(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/payment_cancel.html', {'product': product})
