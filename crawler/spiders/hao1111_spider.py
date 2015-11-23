# -*- coding: utf-8 -*-

import scrapy
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Hao1111Spider(CrawlSpider):
    name = 'hao1111'
    start_urls = ['http://www.hao1111.cn/']
    allowed_domains = ['www.hao1111.cn']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('hao1111')

    deny_pages = [
                    r'http://www\.hao1111\.cn/.*aid=.*'
                 ]

    allow_index = [
                    r'http://www\.hao1111\.cn/.*'
                  ]

    allow_shtml = [
                    r'http://www\.hao1111\.cn/a/.*'
                  ]

    rules = [
                Rule(LinkExtractor(allow=allow_shtml),
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_shtml),
                     process_links=linkfilter.index_filter)
            ]

    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.HAO1111_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//div[@class="article-title"]/h1/text()')
        #loader.add_xpath('title', '//div[class="article-summary"]/text()')
        loader.add_xpath('text', '//div[@class="article-content"]/text()')

        return loader.load_item()


