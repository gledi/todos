from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('pub-key/', views.get_publishable_key, name='pub-key'),
    path('checkout-session/<int:pk>/', views.create_checkout_session, name='checkout-session'),
    path('payment-success/<int:pk>/', views.get_payment_success, name='payment-success'),
    path('payment-cancel/<int:pk>', views.get_payment_cancel, name='payment-cancel'),
]
