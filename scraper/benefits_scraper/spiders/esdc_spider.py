import scrapy
import re

class ESDCSpider(scrapy.Spider):
    name = 'esdc'
    allowed_domains = ['canada.ca']
    custom_settings = {'DEPTH_LIMIT':20}

    def start_requests(self):
        urls = ['https://www.canada.ca/en/employment-social-development.html']
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        # if re.search(r'apply|eligibl|qualify',response.css('main').get(),re.I):
        #     yield {'url': response.url}

        # most viable ?
        if re.search(r'benefit',response.css('title::text').get(),re.I):
            yield {'url':response.url}


        yield from response.follow_all(
            css='a[href*="/services/benefits"][href$="html"]:not([href*="revenue"]):not([href*="defence"])', 
            callback=self.parse
        )
        yield from response.follow_all(
            css='a[href*="/employment-social-development/services"][href$="html"]:not([href*="revenue"]):not([href*="defence"])', 
            callback=self.parse
        )