import scrapy
import re
import os

URLS_OUT_FILE_NAME = os.path.join(os.path.dirname(__file__),'../../../api/data/urls.txt')

class BenefitsSpider(scrapy.Spider):
    name = 'benefits'
    allowed_domains = ['canada.ca',]
    custom_settings = {
        'DEPTH_LIMIT': 3
    }


    def start_requests(self):
        with open(URLS_OUT_FILE_NAME,'w') as f:
            pass

        urls = [
            'https://www.canada.ca/en/services/benefits.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self,response):
        print(response.url)

        if re.search(r'qualify|eligibl|benefit', response.css('h1::text').get(default=''), re.I):
            with open(URLS_OUT_FILE_NAME,'a') as f:
                f.write(response.url+'\n')

        yield from response.follow_all(css='a[href*=benefit][href$=html]', callback=self.parse)
        yield from response.follow_all(css='a[href*=eligibility][href$=html]', callback=self.parse)
        yield from response.follow_all(css='a[href*=qualify][href$=html]', callback=self.parse)
        # yield from response.follow_all(css='a[href*=service][href$=html]', callback=self.parse)