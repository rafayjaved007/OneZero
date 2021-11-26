import csv
import dirtyjson
import requests
from lxml import html


def scrape():
    fieldnames = ['title', 'rating', 'image_url', 'original_price', 'sale_price', 'product_url', 'reviews']
    with open('micro_center.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(1, 5):
            main_url = f'https://www.microcenter.com/search/search_results.aspx?N=4294967288&NTK=all&cat=Laptops/Notebooks-:-MicroCenter&page={page}'
            response = html.fromstring(requests.get(main_url).content)

            for url in response.xpath("//article[@id='productGrid']/ul/li/div[2]//a/@href"):
                res = html.fromstring(requests.get('https://www.microcenter.com'+url).content)

                j = res.xpath("//script[@type='application/ld+json'][3]/text()")[0]
                json_data = dirtyjson.loads(f'''{j}''')
                reviews = []
                try:
                    for i in json_data['review']:
                        reviews.append(i['reviewBody'])
                except:
                    reviews = []

                try:
                    original_price = res.xpath("//div[@id='options-savings']/div/span/text()")[0]
                except IndexError:
                    try:
                        original_price = res.xpath("//div[@id='options-pricing']/span/span/text()")[0]
                    except:
                        original_price = 'N/A'

                try:
                    sale_price = res.xpath("//div[@id='options-pricing']/span/span/text()")[0]
                except:
                    sale_price = 'N/A'

                try:
                    rating = json_data["aggregateRating"]["ratingValue"]
                except:
                    rating = 'N/A'

                try:
                    image_url = res.xpath("//img[@class='productImageZoom']/@src")[0]
                except:
                    image_url = 'N/A'

                data = {
                    'title': res.xpath("//h1/span/span/text()")[0],
                    'sale_price': sale_price,
                    'original_price': original_price,
                    'image_url': image_url,
                    'product_url': 'https://www.microcenter.com' + url,
                    'rating': rating,
                    'reviews': reviews
                }
                writer.writerow(data)


if __name__ ==  '__main__':
    scrape()
