# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from news_crawler.spiders.filters import NewsBloomFilter
from news_crawler.items import NewsItem, NewsLoader


class SohuSpider(CrawlSpider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://www.sohu.com/']
    #nbf = NewsBloomFilter('sohu')

    rules = [Rule(LinkExtractor(allow=(r'http://.*?\.sohu.com/.*?s?html?$'), deny=(r'http://tv.sohu.com/.*')),
                  callback='parse_item', follow=True),#, process_links=nbf.filter_html),
             Rule(LinkExtractor(allow=(r'http://.*?\.sohu.com/.*?/$'), deny=(r'http://tv.sohu.com/.*')))]
                  #process_links=nbf.filter_index)]
    
    def parse_item(self, response):
        loader = NewsLoader(item = NewsItem(), response = response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[contains(@id, "contentText")]//p//text()')
        
        return loader.load_item()
