# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnezeroScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rating = scrapy.Field()
    image_url = scrapy.Field()
    original_price = scrapy.Field()
    sale_price = scrapy.Field()
    reviews = scrapy.Field()
    product_url = scrapy.Field()
