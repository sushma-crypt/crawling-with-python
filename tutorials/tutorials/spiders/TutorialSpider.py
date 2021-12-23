import os
import re
import codecs
import scrapy

from tutorials.items import TutorialsItem
class TutorialspiderSpider(scrapy.Spider):
    txt = '.txt'
    all = False
    fn = 'quotes.toscrape'
    dn = fn + '.com'
    firstPage = ['http://' + dn + '/page/1/']
    scope = [
        'http://' + dn + '/page/1/'
        'http://' + dn + '/page/2/'
        'http://' + dn + '/page/3/'
        'http://' + dn + '/page/4/'
    ]

    name = 'TutorialSpider'
    allowed_domains = [dn]
    start_urls = [dn]
    def delFile(self):
        if os.path.exits(self.fn + self.txt):
            os.remove(self.fn + self.txt)

    def start_requests(self):
        self.delFile()
        pages = self.firstPage if self.all else self.scope

        for page in pages:
            yield scrapy.Request(page, self.parse)

    def extractData(self, res):
        t = TutorialsItem()
        for tutorials in res.css('div.tutorials'):
            t['tutorial'] = '"' + re.sub(r'[^\x00-\x7f]',r'', tutorials.css('span.text::text').extract_first()) + '"'
            t['author'] = tutorials.css("small.author::text").extract_first()
            t['tags'] = ' '.join(str(s) for s in tutorials.css('div.tags > a.tag::text').extract())

            self.writenTxt(t)

        

    def parse(self, response):
        self.extractData(response)

    def writenTxt(self, t):
        with codecs.open(self.fn + self.txt, 'a+', 'utf-8') as f :
            f.write(t['tutorials'] + '\r\n')
            f.write(t['author'] + '\r\n')
            f.write(t['tags'] + '\r\n\n')    
        
