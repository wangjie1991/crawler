# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import Wy163Filter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Wy163Spider(CrawlSpider):
    name = 'wy163'
    allowed_domains = [ 'news.163.com', 
                        'war.163.com', 
                        'sports.163.com', 
                        'ent.163.com', 
                        'money.163.com', 
                        'biz.163.com', 
                        'lady.163.com', 
                        'fashion.163.com', 
                        'tech.163.com', 
                        'jiu.163.com', 
                        'mobile.163.com', 
                        'digi.163.com', 
                        'hea.163.com', 
                        'auto.163.com', 
                        'jiankang.163.com', 
                        'house.163.com', 
                        'discovery.163.com', 
                        'edu.163.com', 
                        'baby.163.com', 
                        'gongyi.163.com'
                      ]
    start_urls = ['http://www.163.com/']
    pathextractor = PathExtractor()
    linkfilter = Wy163Filter('wy163')
    
    rules = [Rule(LinkExtractor(allow=(r'http://[a-z]*\.163\.com/.*?s?html?$')), 
                  callback='parse_item', follow=True, process_links=linkfilter.url_filter), 
             Rule(LinkExtractor(allow=(r'http://[a-z]*\.163\.com/.*?/$')), process_links=linkfilter.index_filter)]

    def parse_item(self, response):
        loader = TextLoader(item = TextItem(), response = response)

        path = self.pathextractor.host(settings.WY163_STORE, response.url)
        loader.add_value('path', path)
        
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//p[contains(@class, "ep-summary")]/text()')
        loader.add_xpath('text', '//div[contains(@id, "endText")]/p//text()')
        
        return loader.load_item()


