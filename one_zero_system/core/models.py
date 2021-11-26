from django.contrib.auth import get_user_model
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    rating = models.FloatField(null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    sale_price = models.FloatField(null=True, blank=True)
    polarity = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    product_url = models.URLField()
    word_counter = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title
