import scrapy


class BooksItem(scrapy.Item):
    
    title = scrapy.Field()
    price = scrapy.Field()
    imageurl = scrapy.Field()
    bookurl = scrapy.Field()

