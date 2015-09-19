# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from news_crawler.spiders.filters import NewsBloomFilter
from news_crawler.items import NewsItem, NewsLoader


class QQSpider(CrawlSpider):
    name = 'qq'
    allowed_domains = ['qq.com']
    start_urls = ['http://www.qq.com/']
    deny_urls = [r'http://v.qq.com/.*']
    #nbf = NewsBloomFilter('qq')
    
    rules = [Rule(LinkExtractor(allow=(r'http://.*?\.qq.com/.*?s?html?$'), deny=(deny_urls)),
                  callback='parse_item', follow=True, ),#process_links=nbf.filter_html),
             Rule(LinkExtractor(allow=(r'http://.*?\.qq.com/.*?/$'), deny=(deny_urls)), )]#process_links=nbf.filter_index)]
    
    def parse_item(self, response):
        loader = NewsLoader(item = NewsItem(), response = response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[contains(@id, "Cnt-Main-Article-QQ")]/p[contains(@style, "TEXT-INDENT: 2em")]//text()')
        
        return loader.load_item()
