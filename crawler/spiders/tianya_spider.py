# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class TianyaSpider(CrawlSpider):
    name = 'tianya'
    start_urls = ['http://bbs.tianya.cn/']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('tianya')

    allowed_domains = ['bbs.tianya.cn']
    allow_index = [r'http://bbs\.tianya\.cn/list.*']
    allow_shtml = [r'http://bbs\.tianya\.cn/post-.*']

    rules = [
                Rule(LinkExtractor(allow=allow_shtml), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter), 
                Rule(LinkExtractor(allow=allow_index), 
                     process_links=linkfilter.index_filter)
            ]

    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.tianya(settings.TY_STORE, response)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1//text()')
        loader.add_xpath('text', '//div[contains(@class, "bbs-content")]/text()')

        return loader.load_item()


