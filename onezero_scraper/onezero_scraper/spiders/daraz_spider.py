import json

import scrapy

from ..items import FYPItem


class DarazSpider(scrapy.Spider):
    name = "daraz_spider"
    page_num = 88
    pre = 'https://www.noon.com/_svc/catalog/api/u/'
    start_urls = [
        f"https://www.daraz.pk/smartphones/?page={page_num}&spm=a2a0e.searchlist.cate_1.1.123c185bvlGPp9"
    ]
    pages_to_scrape = 89

    regex_for_product = 'app.run(...)+\)\;'
    regex_for_list = 'window.pageData=(...)*\W\}{3}'

    def parse(self, response):
        text = response.text
        product_data = text[text.find('window.pageData='):]
        product_data = product_data[:product_data.find('}}}')]
        product_data = product_data.replace('window.pageData=', '')
        product_data = product_data+'}}}'

        for item in json.loads(product_data)['mods']['listItems']:
            yield response.follow(url=item['productUrl'], callback=self.parse_product, meta={'url': item['productUrl']})

        next_page = f'https://www.daraz.pk/smartphones/?page={self.page_num}&spm=a2a0e.searchlist.cate_1.1.123c185bvlGPp9'

        if self.page_num <= self.pages_to_scrape:
            self.page_num += 1
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        try:
            items = FYPItem()
            reviews = []
            url = response.meta.get('url')
            product_data = response.text[response.text.find('app.run'):]
            product_data = product_data[:product_data.find('}}})')]
            product_data = product_data.replace('app.run(', '')
            product_data = product_data + '}}}'
            product_data = json.dumps(product_data)
            data = json.loads(json.loads(product_data))

            items['title'] = data['data']['root']['fields']['product']['title']
            items['rating'] = data['data']['root']['fields']['review']['ratings']['average']
            items['image_url'] = data['data']['root']['fields']['skuInfos']['0']['image']
            items['product_url'] = url

            if 'originalPrice' in data['data']['root']['fields']['skuInfos']['0']['price']:
                items['original_price'] = data['data']['root']['fields']['skuInfos']['0']['price']['originalPrice']['value']
                items['sale_price'] = data['data']['root']['fields']['skuInfos']['0']['price']['salePrice']['value']
            else:
                items['original_price'] = data['data']['root']['fields']['skuInfos']['0']['price']['salePrice']['value']
                items['sale_price'] = ''

            for review in data['data']['root']['fields']['review']['reviews']:
                reviews.append(review['reviewContent'])
            items['reviews'] = reviews

            yield items
        except json.decoder.JSONDecodeError:
            pass
