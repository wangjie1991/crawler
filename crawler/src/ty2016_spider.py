# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Ty2016Spider(CrawlSpider):
    name = 'ty2016'
    start_urls = ['http://www.ty2016.com/']
    allowed_domains = ['www.ty2016.com', 'wx.ty2016.com']

    linkfilter = LinkFilter('ty2016')
    pathextractor = PathExtractor()

    rules = [
                Rule(LinkExtractor(allow=[r'http://www\.ty2016\.com/.*/$', r'http://wx\.ty2016\.com/.*/$']), 
                     process_links=linkfilter.index_filter),
                Rule(LinkExtractor(allow=r'http://www\.ty2016\.com/.*\.s?html?$'), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=r'http://wx\.ty2016\.com/.*\.s?html?$'), 
                     callback='parse_wx', follow=True, 
                     process_links=linkfilter.html_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)
        path = self.pathextractor.host(settings.TY2016_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[contains(@id, "main")]//p//text()')
        item = loader.load_item()
        
        if ('text' not in item) or (item['text'] == ''):
            with open('url.txt', 'a') as url_file:
                url = response.url + '\n'
                url_file.write(url.encode('utf-8'))
        
        return item

    def parse_wx(self, response):
        loader = TextLoader(item=TextItem(), response=response)
        path = self.pathextractor.host(settings.TY2016_STORE, response.url)
        loader.add_value('path', path)
        loader.add_value('title', '')
        loader.add_xpath('text', '//p//text()')
        item = loader.load_item()
        
        if ('text' not in item) or (item['text'] == ''):
            with open('url.txt', 'a') as url_file:
                url = response.url + '\n'
                url_file.write(url.encode('utf-8'))
        
        return item

