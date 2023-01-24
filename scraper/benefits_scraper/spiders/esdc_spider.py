import scrapy
import re

partial_link_css_selector = lambda *args: f'a{"".join(args)}[href$="html"]:not([href*="revenue"]):not([href*="defence"])'

class ESDCSpider(scrapy.Spider):
    name = 'esdc'
    allowed_domains = ['canada.ca']
    custom_settings = {'DEPTH_LIMIT':20}

    def start_requests(self):
        urls = ['https://www.canada.ca/en/employment-social-development.html']
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response, possible_benefit=False):
        ## only check if apply, eligibl(e|ity), qualify in <main> => too many false positives
        # if re.search(r'apply|eligibl|qualify',response.css('main').get(),re.I):
        #     yield {'url': response.url}

        # most viable (assumes 'benefit' is in the title and there's a next or previous button for navigation) ?
        if possible_benefit or re.search(r'benefit',response.css('title::text').get(),re.I) and any(re.search(r'next|previous',b,re.I) for b in response.css('a::text').getall()):
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