import scrapy
from scrapy import linkextractors
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CoolSpider(CrawlSpider):
    name = 'website.com'
    allowed_domains = ['website.com']
    start_urls = ['http://www.website.com']

    rules = (
        Rule(LinkExtractor(allow=('product\.php',)), callback='parse_item'),

    )
    def parse_item(self, response):
        item = scrapy.Item()
        item['name'] = response.xpath('//td@id="prod_name"]/text()').get()
        item['link_text'] = response.meta['link_text']
        return item
