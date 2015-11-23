# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class Wy163Spider(CrawlSpider):
    name = 'wy163'
    start_urls = ['http://www.163.com/']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('wy163')

    allowed_domains = [
                        'gongyi.163.com', 
                        'baby.163.com', 
                        'edu.163.com', 
                        'house.163.com', 
                        'jiankang.163.com', 
                        'auto.163.com', 
                        'hea.163.com', 
                        'digi.163.com', 
                        'mobile.163.com', 
                        'jiu.163.com', 
                        'tech.163.com', 
                        'fashion.163.com', 
                        'lady.163.com', 
                        'biz.163.com', 
                        'money.163.com', 
                        'ent.163.com', 
                        'sports.163.com', 
                        'data.163.com', 
                        'view.163.com', 
                        'war.163.com', 
                        'news.163.com', 
                        'www.163.com'
                      ]

    deny_pages = [
                    r'.*keyword.*', 
                    r'.*photoview.*'
                 ]

    allow_index = [r'http://[a-z]*\.163\.com/.*/$']
    allow_shtml = [r'http://[a-z]*\.163\.com/.*s?html?$']
    allow_spec = [r'http://[a-z]*\.163\.com/.*special.*s?html?$']
    allow_view = [r'http://view\.163\.com/.*s?html?$']

    rules = [
                Rule(LinkExtractor(allow=allow_shtml, 
                                   deny=deny_pages+allow_spec+allow_view), 
                     callback='parse_shtml', follow=True, 
                     process_links=linkfilter.html_filter), 
                Rule(LinkExtractor(allow=allow_spec, deny=deny_pages), 
                     callback='parse_spec', follow=True, 
                     process_links=linkfilter.html_filter), 
                Rule(LinkExtractor(allow=allow_view, deny=deny_pages+allow_spec), 
                     callback='parse_view', follow=True, 
                     process_links=linkfilter.html_filter), 
                Rule(LinkExtractor(allow=allow_index, deny=deny_pages), 
                     process_links=linkfilter.index_filter)
            ]

    def parse_shtml(self, response):
        loader = TextLoader(item = TextItem(), response = response)

        path = self.pathextractor.host(settings.WY163_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')

        ps = response.xpath('//div[@id="endText"]/p')
        # old pages:http://news.163.com/05/0130/10/1BBB83S30001121Q.html
        if not ps:
            ps = response.xpath('//div[@id="text"]/p')
        if not ps:
            ps = response.xpath('//div[@id="content"]/p')

        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()

    def parse_spec(self, response):
        loader = TextLoader(item = TextItem(), response = response)
        path = self.pathextractor.host(settings.WY163_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//h2/text()')
        loader.add_xpath('text', '//h3/text()')
        
        ps = response.xpath('//p')
        for p in ps:
            ts = p.xpath('./text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()

    def parse_view(self, response):
        loader = TextLoader(item = TextItem(), response = response)
        path = self.pathextractor.host(settings.WY163_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h3/text()')
        loader.add_xpath('text', '//div[@class="feed-text"]/p/text()')
        return loader.load_item()


