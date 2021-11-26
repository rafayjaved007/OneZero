import csv
import json

import requests
import scrapy
from lxml import html

from ..items import OnezeroScraperItem


class BestBuySpider(scrapy.Spider):
    name = "bestbuy_spider"
    page_num = 1

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'authority': 'www.bestbuy.com',
        'sec-ch-ua': '"Opera";v="77", "Chromium";v="91", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.bestbuy.com/site/computers-pcs/laptop-computers/abcat0502000.c?id=abcat0502000&intl=nosplash',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': 'SID=11a1807f-c62d-4c14-bce5-a5a974c13df0; bm_sz=D29DD2552AECD5E4D1667BE0D1C7B9E0~YAAQL54QAjD0bO16AQAA9bVLKgzLj3gTkjvRvJbELhrUtEDOoRGHWff/8fYP9v9SIYz78km/w/0DhDcxNRnBA0zQSXlwkm0q8IkF0LDgdsLeeIVBdzKgZyR30hnCrg8ywaSZO4QObTf4fKQpnLcSzMroeTASO5/Tbka4r+tDyMyrCaiAifv28hr6tDM9ERQt7Qbw0g8zQvqdz23RInpgH05BbdWJsqw480ea0KB+OY8TfCfa6VY0Yj+OTf+bJas7WCn4uyz1iVowdKQvNrnlJdJYxQw9nu8GuOMT5Iw35zwk4+2GzwwoKpSMs+FgzqrFnBjYBaX9xOGXmBFeQLMxEVXeUQvtgU/8BEwycUUMonJUx7vHLsasmNSyntySv0LNtDA92+DPGCwg18KC2xpt2A==~3420227~4342323; bby_rdp=l; CTT=d970133291f6d5f495f392dde8454c81; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; _abck=97C05977F15D7E358FB50CC99EE7ED84~0~YAAQL54QAk70bO16AQAAG89LKgbqmQXyxlKd4603WAPY57gtBfs/W3Q9cqhgBomRPClyScsyxPvCM6z8m9+wOZ3kOlpnhhBiGguqw251NV9nBoUJ+T1uBj3kgf8RWC3FN7lWTMO6bpNxyNwZKdXIE4PZ4cBgI/s9LsMCWpeyCmHn6etVyYbHdPTdY11TNyUXB5VAKl7iwzYVFKGm3ScifJ6POrZu8Yuq8xQ7EvexqsmMGBO4syrPx3XGuzTjN83tfPrUNOoaX+msAyYKQTspA8U4iW7xcIryg5gDgcC9lVK/tHMo/xpzeyY14ECIMTS1RRSg0ane/YgbWW03/0KYu1hlT5UnTkc3/THc9QOMKcAJxnyJ3p0Mm/sD/uIm3r/xzyx5bk1qi6nzgq2cHWJ/pR9sYAflMUrRjF5anMiA8+hsSQfqabKM8RTtSzlPwQA=~-1~||-1||~-1; intl_splash=false; intl_splash=false; oid=986209249; vt=46eea450-f8f6-11eb-93d6-12d7132a90df; rxVisitor=1628502224169OGTC0VFRC78H366N2TN1K368R3E6LF1T; COM_TEST_FIX=2021-08-09T09%3A43%3A45.851Z; basketTimestamp=1628502227215; AMCVS_F6301253512D2BDB0A490D45%40AdobeOrg=1; _cs_mk=0.49109049633497714_1628502230800; s_cc=true; locDestZip=96939; locStoreId=852; sc-location-v2=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222021-08-09T09%3A43%3A51.539Z%22%2C%22ModifiedAt%22%3A%222021-08-09T09%3A43%3A51.637Z%22%2C%22ExpiresAt%22%3A%222022-08-09T09%3A43%3A51.637Z%22%7D%2C%22value%22%3A%22%7B%5C%22physical%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2296939%5C%22%2C%5C%22source%5C%22%3A%5C%22A%5C%22%2C%5C%22captureTime%5C%22%3A%5C%222021-08-09T09%3A43%3A51.535Z%5C%22%7D%2C%5C%22destination%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2296939%5C%22%7D%2C%5C%22store%5C%22%3A%7B%5C%22storeId%5C%22%3A852%2C%5C%22zipCode%5C%22%3A%5C%2296701%5C%22%2C%5C%22storeHydratedCaptureTime%5C%22%3A%5C%222021-08-09T09%3A43%3A51.637Z%5C%22%7D%7D%22%7D; dtSa=-; dtCookie=v_4_srv_9_sn_GJIGQ7F8MFOVS41RP4D3CPAFAMRQLB39_app-3Aea7c4b59f27d43eb_1_app-3A1b02c17e3de73d2a_1_ol_0_perc_100000_mul_1; CTE5=T; CTE22=T; _cs_c=1; CTE8=T; bby_cbc_lb=p-browse-e; ltc=%20; bby_prc_lb=p-prc-w; IMPRESSION=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222021-08-09T10%3A32%3A59.855Z%22%2C%22ModifiedAt%22%3A%222021-08-09T11%3A08%3A23.104Z%22%2C%22ExpiresAt%22%3Anull%7D%2C%22value%22%3A%7B%22data%22%3A%5B%7B%22contextData%22%3A%7B%22bb.loadTime%22%3A3537%7D%7D%5D%7D%7D; s_sq=%5B%5BB%5D%5D; rxvt=1628509165718|1628506978102; dtPC=9$107358193_701h-vNPPETWBUBHFQDHPNFMFEQJTWHWUMSVDV-0e3; c2=Computers%20%26%20Tablets%3A%20Laptops%3A%20All%20Laptops; AMCV_F6301253512D2BDB0A490D45%40AdobeOrg=1585540135%7CMCMID%7C31744267641648354137250308613278895670%7CMCAID%7CNONE%7CMCOPTOUT-1628514568s%7CNONE%7CvVersion%7C4.4.0; dtLatC=1; _cs_id=1b617a48-9068-a0f9-de5b-8bf198a7c7ae.1628502262.3.1628507380.1628507148.1614963257.1662666262840.Lax.0; _cs_s=3.1'
    }

    def start_requests(self):
        fieldnames = ['title', 'rating', 'image_url', 'original_price', 'sale_price', 'product_url', 'reviews']
        with open('bestbuy.csv', 'w', encoding='UTF-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for page in range(1, 49):
                site_url = f'https://www.bestbuy.com/site/laptop-computers/all-laptops/pcmcat138500050001.c?id=pcmcat138500050001&cp={page}'
                res = requests.get(site_url, headers=self.headers)
                response = html.fromstring(res.content)
                product_urls = response.xpath("//h4[@class='sku-header']/a/@href")
                for url in product_urls:
                    link = 'https://www.bestbuy.com'+url
                    response = html.fromstring(requests.get(url=link, headers=self.headers).content)
                    reviews_url = url.replace('/site', 'https://www.bestbuy.com/site/reviews')
                    reviews = self.get_reviews(reviews_url.replace('.p', ''))
                    try:
                        original_price = response.xpath("//div[@class='pricing-price__regular-price']/text()")[0].split(' ')[1]
                    except:
                        original_price = response.xpath("//div[@class='priceView-hero-price priceView-customer-price']/span/text()")[0]

                    try:
                        rating = response.xpath("//span[@class='ugc-c-review-average']/text()")[0]
                    except:
                        rating = 'N/A'

                    try:
                        image_url = response.xpath("//div[@class='item image-wrapper']/button/img/@src")[0]
                    except:
                        image_url = response.xpath("//div[@class='primary-image-grid'][1]//img/@src")[0]
                    data = {
                    'title': response.xpath("//h1/text()")[0],
                    'rating': rating,
                    'image_url': image_url,
                    'original_price': original_price,
                    'sale_price': response.xpath("//div[@class='priceView-hero-price priceView-customer-price']/span/text()")[0],
                    'product_url': link,
                    'reviews': reviews
                    }

                    writer.writerow(data)

    #     if self.page_num <= self.pages_to_scrape:
    #         self.page_num += 1
    #         yield scrapy.Request(url=next_page, callback=self.parse)

    def get_reviews(self, url):
        c = True
        reviews_list = []
        page = 1
        while c and len(reviews_list) <= 500:
            reviews_resp = html.fromstring(requests.get(url+f'&page={page}', headers=self.headers).content)
            reviews_list = reviews_list + reviews_resp.xpath("//div[@class='ugc-review-body body-copy-lg']//p/text()")
            try:
                if reviews_resp.xpath("//li[@class='page next disabled']/a/@class")[0] == " disabled":
                    c = False
            except IndexError:
                page += 1

        return reviews_list
