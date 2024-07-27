from django.contrib import admin

from .models import Product, Picture


class PictureInline(admin.TabularInline):
    model = Picture
    min_num = 1
    max_num = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    list_editable = ('price', 'currency')
    inlines = [PictureInline]
