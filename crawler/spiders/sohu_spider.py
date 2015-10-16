# -*- coding: utf-8 -*-

import scrapy
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class SohuSpider(CrawlSpider):
    name = 'sohu'
    start_urls = ['http://www.sohu.com/']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('sohu')
    
    allowed_domains = [
                        'city.sohu.com',
                        'caipiao.sohu.com',
                        'mgame.sohu.com',
                        'yule.sohu.com',
                        'gongyi.sohu.com',
                        'chihe.sohu.com',
                        'baobao.sohu.com',
                        'learning.sohu.com',
                        'travel.sohu.com',
                        'health.sohu.com',
                        'fashion.sohu.com',
                        'auto.sohu.com',
                        'chuangke.sohu.com',
                        'it.sohu.com',
                        'fund.sohu.com',
                        'stock.sohu.com',
                        'money.sohu.com',
                        'business.sohu.com',
                        'sports.sohu.com',
                        'book.sohu.com',
                        'history.sohu.com',
                        'cul.sohu.com',
                        'mil.sohu.com',
                        'news.sohu.com',
                        'www.sohu.com'
                      ]

    deny_pages = [
                    r'http://auto\.sohu\.com/.*video.*', 
                    r'http://news\.sohu\.com/.*shuzi-.*', 
                    r'http://news\.sohu\.com/matrix/', 
                    r'http://pic.*'
                 ]

    allow_index = [
                    r'http://music\.yule\.sohu\.com/.*', 
                    r'http://db\.auto\.sohu\.com/.*', 
                    r'http://digi\.it\.sohu\.com/.*', 
                    r'http://[a-z]*\.sports\.sohu\.com/.*', 
                    r'http://star\.news\.sohu\.com/.*', 
                    r'http://[a-z]*\.sohu\.com/.*' 
                  ]

    allow_shtml = [
                    r'http://music\.yule\.sohu\.com/[\d]*/.*\.s?html$', 
                    r'http://db\.auto\.sohu\.com/[\d]*/.*\.s?html$', 
                    r'http://digi\.it\.sohu\.com/[\d]*/.*\.s?html$', 
                    r'http://star\.news\.sohu\.com/[\d]*/.*\.s?html$', 
                    r'http://[a-z]*\.sohu\.com/[\d]*/.*\.s?html$'
                  ]

    allow_comnt = [
                    r'http://book\.sohu\.com/s[\d]*/.*',
                    r'http://cul\.sohu\.com/s[\d]*/.*',
                    r'http://star\.news\.sohu\.com/s[\d]*/.*/$', 
                    r'http://news\.sohu\.com/.*newsmaker.*\.s?html$', 
                    r'http://news\.sohu\.com/.*dianji.*\.s?html$'
                  ]
 
    rules = [
                Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages),
                     callback='parse_shtml', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_comnt, deny=deny_pages),
                     callback='parse_comnt', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_shtml+allow_comnt+deny_pages),
                     process_links=linkfilter.index_filter)
            ]

    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.SOHU_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')

        ps = response.xpath('//div[contains(@id, "contentText")]//p')
        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()

    def parse_comnt(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.SOHU_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('title', '//h2/text()')
        loader.add_xpath('title', '//h3/text()')

        ps = response.xpath('//p')
        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()


