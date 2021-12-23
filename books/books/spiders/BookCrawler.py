import codecs

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule




class BookcrawlerSpider(CrawlSpider):
    name = 'BookCrawler'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(allow=r'catalogue/category'), callback='parsepage', follow=True),
    )

    def parsepage(self, res):
        bk = ()
        books = res.xpath('//article[@class="product_pod"]')

        for b in books:

            bk['title'] = b.xpath('.//h3/a/@title').extract_first()
            bk['price'] = b.xpath('.//div/p[@class="price_color"]/text()').extract_first()
            bk['imageurl'] = self.start_urls[0] + b.xpath('.//img[@class="thumbnail"]/@src').extract_first().replace('../', '')
            bk['bookurl'] = self.start_urls[0] + b.path('.//h3/a/@href').extract_first().replace('../','')

            with codecs.open('books.txt', 'a+', 'utf-8') as f:
                f.write(bk['title'] + '\r\n')
                f.write(bk['price'] + '\r\n')
                f.write(bk['imageurl'] + '\r\n')
                f.write(bk['bookurl'] + '\r\n\r\n')
