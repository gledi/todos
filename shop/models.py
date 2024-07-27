from django.db import models


class Product(models.Model):    # shop_product
    class Currency(models.TextChoices):
        EUR = 'EUR', '€'
        USD = 'USD', '$'
        ALL = 'ALL', 'L'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.EUR)

    stripe_product_id = models.CharField(max_length=100, blank=True)
    stripe_price_id = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

    @property
    def primary_picture(self):
        pic = self.pictures.first()
        if pic:
            return pic.photo.url
        return '/static/images/noproduct.png'


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    photo = models.ImageField(upload_to='products')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'pictures'

    def __str__(self):
        if self.caption:
            return self.caption
        return self.photo.name
