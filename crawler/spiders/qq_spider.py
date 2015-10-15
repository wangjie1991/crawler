# -*- coding: utf-8 -*-

import scrapy
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class QQSpider(CrawlSpider):
    name = 'qq'
    start_urls = ['http://www.qq.com/']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('qq')
    sep = ''

    allowed_domains = [
                        'mil.qq.com',
                        'yue.qq.com',
                        'thinker.qq.com',
                        'baby.qq.com',
                        'gongyi.qq.com',
                        'edu.qq.com',
                        'cul.qq.com',
                        'space.qq.com',
                        'digi.tech.qq.com',
                        'tech.qq.com',
                        'house.qq.com',
                        'auto.qq.com',
                        'health.qq.com',
                        'lady.qq.com',
                        'fashion.qq.com',
                        'ent.qq.com',
                        'sports.qq.com',
                        'stock.qq.com',
                        'finance.qq.com',
                        'news.qq.com'
                      ]

    deny_pages = [
                 ]

    allow_index = [
                    r'http://view\.news\.qq.com/.*',
                    r'http://[a-z]*\.auto\.qq\.com/.*',
                    r'http://[a-z]*\.house\.qq\.com/.*',
                    r'http://[a-z]*\.qq.com/.*'
                  ]

    allow_a = [
                r'http://[a-z]*\.auto\.qq\.com/a/.*\.s?html?$',
                r'http://[a-z]*\.house\.qq\.com/a/.*\.s?html?$',
                r'http://[a-z]*\.qq\.com/a/.*\.s?html?$'
              ]

    allow_original = [
                        r'http://view\.news\.qq\.com/original/.*\.s?html?$',
                        r'http://[a-z]*\.qq\.com/original/.*\.s?html?$'
                     ]

    
    rules = [
                Rule(LinkExtractor(allow=allow_a),
                     callback='parse_a', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_original),
                     callback='parse_original', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_a+allow_original),
                    process_links=linkfilter.index_filter)
            ]

    def parse_a(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.QQ_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')

        ps = response.xpath('//div[contains(@id, "Cnt-Main-Article-QQ")]/p[contains(@style, "TEXT-INDENT: 2em")]')
        if not ps:
            ps = response.xpath('//div[contains(@id, "Cnt-Main-Article-QQ")]/p')

        for p in ps:
            if p.xpath('./script'):
                continue
            ts = p.xpath('.//text()').extract()
            text = self.sep.join(ts)
            loader.add_value('text', text)

        return loader.load_item()

    def parse_original(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.QQ_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[contains(@class, "daoyu")]//div[contains(@class, "intr")]/text()')
        loader.add_xpath('text', '//div[contains(@id, "articleContent")]/h2/text()')
        loader.add_xpath('text', '//div[contains(@id, "articleContent")]/h3/text()')
        loader.add_xpath('text', '//div[contains(@id, "articleContent")]/p/text()')
        loader.add_xpath('text', '//div[contains(@class, "jieyu")]//text()')

        return loader.load_item()

