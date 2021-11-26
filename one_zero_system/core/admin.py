from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_price', 'sale_price', 'website', 'rating')
    list_filter = ('website', 'original_price', 'sale_price', 'polarity')
    search_fields = ['title', 'website']


admin.site.register(Product, ProductAdmin)
