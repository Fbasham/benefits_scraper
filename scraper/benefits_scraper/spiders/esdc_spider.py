import scrapy
import re

partial_link_css_selector = lambda *args: f'a{"".join(args)}[href$="html"]:not([href*="revenue"]):not([href*="defence"])'

class ESDCSpider(scrapy.Spider):
    name = 'esdc'
    allowed_domains = ['canada.ca']
    custom_settings = {'DEPTH_LIMIT':30}

    def start_requests(self):
        urls = ['https://www.canada.ca/en/employment-social-development.html']
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response, possible_benefit=False):

        if possible_benefit or re.search(r'benefit',response.css('title::text').get(),re.I) or\
            any(re.search(r'benefit',h,re.I) for h in response.css('h1::text').getall()) or\
            any(re.search(r'next|previous',b,re.I) for b in response.css('a::text').getall()) or\
            any(re.search(r'benefit',m.attrib.get('content',''),re.I) for m in response.css('meta')):

            # flag the page as a probable benefit and yield to the output
            possible_benefit = True
            yield {'url':response.url}


        yield from response.follow_all(
            css=partial_link_css_selector('[href*="/services/benefits"]'),
            callback=lambda *args: self.parse(*args, possible_benefit=possible_benefit)
        )
        yield from response.follow_all(
            css=partial_link_css_selector('[href*="/employment-social-development/services"]'), 
            callback=lambda *args: self.parse(*args, possible_benefit=possible_benefit)
        )