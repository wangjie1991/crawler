# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Wy163Spider(CrawlSpider):
    name = 'baike'
    start_urls = ['http://baike.baidu.com/']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('baike')

    allowed_domains = ['baike.baidu.com']
    allow_index = [ r'http://baike\.baidu\.com/.*/$' ]
    allow_shtml = [
                    r'http://baike\.baidu\.com/.*#viewPageContent$', 
                    r'http://baike\.baidu\.com/.*htm$'
                  ]

    rules = [
                Rule(LinkExtractor(allow=allow_shtml), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter), 
                Rule(LinkExtractor(allow=allow_index), 
                     process_links=linkfilter.index_filter)
            ]

    def parse_item(self, response):
        loader = TextLoader(item = TextItem(), response = response)

        path = self.pathextractor.baike(settings.BAIKE_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//h2//text()')
        loader.add_xpath('text', '//h3//text()')

        ds = response.xpath('//div[@class="para"]')
        for d in ds:
            ts = d.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()


