import scrapy
import re
import os

data_fn = os.path.join(os.path.dirname(__file__),'../../../api/data.txt')

class BenefitsSpider(scrapy.Spider):
    name = 'benefits'
    custom_settings = {
        'DEPTH_LIMIT': 3
    }

    def start_requests(self):
        with open(data_fn,'w') as f:
            pass

        urls = [
            'https://www.canada.ca/en/services/benefits.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self,response):
        print(response.url)

        if re.search(r'qualify|eligible|eligibility', response.css('h1::text').get(default=''), re.I):
            with open(data_fn,'a') as f:
                f.write(response.url+'\n')

        yield from response.follow_all(css='a[href*=benefit][href$=html]', callback=self.parse)
        yield from response.follow_all(css='a[href*=eligibility][href$=html]', callback=self.parse)
        yield from response.follow_all(css='a[href*=qualify][href$=html]', callback=self.parse)
        # yield from response.follow_all(css='a[href*=service][href$=html]', callback=self.parse)