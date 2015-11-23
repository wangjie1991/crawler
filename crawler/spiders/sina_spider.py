# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class SinaSpider(CrawlSpider):
    name = 'sina'
    start_urls = ['http://sina.com.cn']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('sina')

    allowed_domains = [
                        'gongyi.sina.com.cn',
                        'lottery.sina.com.cn',
                        'collection.sina.com.cn',
                        'health.sina.com.cn',
                        'book.sina.com.cn',
                        'jiaju.sina.com.cn',
                        'baby.sina.com.cn', 
                        'edu.sina.com.cn', 
                        'fashion.sina.com.cn', 
                        'history.sina.com.cn', 
                        'zhuanlan.sina.com.cn', 
                        'yue.sina.com.cn',
                        'ent.sina.com.cn', 
                        'run.sina.com.cn',
                        'sports.sina.com.cn', 
                        'shiqu.sina.com.cn',
                        'mobile.sina.com.cn',
                        'digi.sina.com.cn',
                        'chuangye.sina.com.cn',
                        'tech.sina.com.cn', 
                        'finance.sina.com.cn', 
                        'news.sina.com.cn', 
                        'www.sina.com.cn' 
                      ]

    deny_pages = [
                    r'http://sports\.sina\.com\.cn/focus//.*', 
                    r'http://news\.jiaju\.sina\.com\.cn/search.*', 
                    r'http://tech\.sina\.com\.cn//.*', 
                    r'http://sports\.sina\.com\.cn//.*', 
                    r'http://book.sina.com.cn/z/.*', 
                    r'http://fashion\.sina\.com\.cn/match/.*', 
                    r'http://fashion\.sina\.com\.cn/home/.*', 
                    r'http://finance\.sina\.com\.cn/sf/.*', 
                    r'.*try.*', 
                    r'.*blog.*', 
                    r'.*bss.*', 
                    r'.*club.*', 
                    r'.*photo.*', 
                    r'.*video.*'
                 ]

    allow_index = [
                    r'http://news.jiaju.sina.com.cn/.*',
                    r'http://kid\.baby\.sina\.com\.cn/',
                    r'http://cul\.history\.sina\.com.\cn/.*/$', 
                    r'http://weather\.news\.sina\.com.\cn/.*/$', 
                    r'http://sky\.news\.sina\.com.\cn/.*/$', 
                    r'http://mil\.news\.sina\.com.\cn/.*/$', 
                    r'http://[a-z]*\.sina\.com\.cn/.*/$', 
                    r'http://roll\.[a-z]\.sina\.com.\cn/.*'
                  ]

    allow_shtml = [
                    r'http://cul\.history\.sina\.com.\cn/.*\.s?html$', 
                    r'http://weather\.news\.sina\.com.\cn/.*\.s?html$', 
                    r'http://sky\.news\.sina\.com.\cn/.*\.s?html$', 
                    r'http://mil\.news\.sina\.com.\cn/.*\.s?html$', 
                    r'http://[a-z]*\.sina\.com\.cn/.*\.s?html$'
                 ]
    
    rules = [
                Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=deny_pages), 
                     process_links=linkfilter.index_filter)
            ]

    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.SINA_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('text', '//h1/text()')
        
        ps = response.xpath('//div[@id="artibody"]//p')
        if not ps:
            ps = response.xpath('//div[@id="article"]//p')

        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)
        
        return loader.load_item()


