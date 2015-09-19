# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from news_crawler.spiders.filters import NewsBloomFilter
from news_crawler.items import NewsItem, NewsLoader


class W163Spider(CrawlSpider):
    name = '163'
    allowed_domains = ['163.com']
    start_urls = ['http://www.163.com/']
    deny_urls = [r'http://open.163.com/.*', r'http://v.163.com/.*', r'http://g.163.com/.*']
    #nbf = NewsBloomFilter('w163')
    
    rules = [Rule(LinkExtractor(allow=(r'http://.*?\.163.com/.*?s?html?$'), deny=(deny_urls)),
                  callback='parse_item', follow=True, ),#process_links=nbf.filter_html),
             Rule(LinkExtractor(allow=(r'http://.*?\.163.com/.*?/$'), deny=(deny_urls)))]#, process_links=nbf.filter_index)]
    
    def parse_item(self, response):
        loader = NewsLoader(item = NewsItem(), response = response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[contains(@id, "endText")]/p//text()')
        
        return loader.load_item()
