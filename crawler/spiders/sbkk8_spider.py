# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Sbkk8Spider(CrawlSpider):
    name = 'sbkk8'
    start_urls = ['http://www.sbkk8.cn/mingzhu/']
    allowed_domains = ['www.sbkk8.cn']

    linkfilter = LinkFilter('sbkk8')
    pathextractor = PathExtractor()

    rules = [
                Rule(LinkExtractor(allow=r'http://www\.sbkk8\.cn/mingzhu/.*/$'), 
                     process_links=linkfilter.index_filter),
                Rule(LinkExtractor(allow=r'http://www\.sbkk8\.cn/mingzhu/.*\.html$'), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.SBKK8_STORE, response.url)
        loader.add_value('path', path)

        loader.add_xpath('title', '//h1/text()')

        loader.add_xpath('text', '//div[contains(@id, "f_article")]//p//text()')
        loader.add_xpath('text', '//div[contains(@id, "f_article")]/div/text()')
        loader.add_xpath('text', '//div[contains(@id, "f_article")]/text()')
        
        loader.add_xpath('text', '//div[contains(@id, "articleText")]//p//text()')

        item = loader.load_item()
        
        if (item['text'] == ''):
            with open('url.txt', 'a') as url_file:
                url = response.url + '\n'
                url_file.write(url.encode('utf-8'))
        
        return item


