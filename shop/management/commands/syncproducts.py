from decimal import Decimal

from stripe import StripeClient
from django.conf import settings
from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Synchronizes product data with stripe'

    def handle(self, *args, **options):
        stripe = StripeClient(settings.STRIPE_SECRET_KEY)

        resp = stripe.products.list({
            "active": True,
            "expand": ["data.default_price"],
        })

        for item in resp.auto_paging_iter():
            item_price = item['default_price']
            currency = Product.Currency(item_price['currency'].upper())
            price_whole = item_price['unit_amount'] // 100
            price_fraction = item_price['unit_amount'] % 100
            price = Decimal(f'{price_whole}.{price_fraction:02}')

            product, created = Product.objects.update_or_create(
                stripe_product_id=item['id'],
                defaults={
                    'name': item['name'],
                    'description': item['description'],
                    'price': price,
                    'currency': currency,
                    'stripe_price_id': item_price['id'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated product: {product}'))
