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
                        #'house.qq.com',
                        #'auto.qq.com',
                        'health.qq.com',
                        'lady.qq.com',
                        'fashion.qq.com',
                        'ent.qq.com',
                        'sports.qq.com',
                        'stock.qq.com',
                        'finance.qq.com',
                        'history,qq.com',
                        'news.qq.com',
                        'www.qq.com'
                      ]

    deny_pages = [
                    r'http://bss\.auto\.qq\.com/.*',
                    r'http://club\.auto\.qq\.com/.*',
                    r'http://comment\.auto\.qq\.com/.*',
                    r'http://data\.auto\.qq\.com/.*',
                    r'http://uc\.auto\.qq\.com/.*',
                    r'http://bss\.house\.qq\.com/.*',
                    r'http://db\.house\.qq\.com/.*'
                 ]

    allow_index = [
                    r'http://view\.news\.qq.com/.*',
                    r'http://[a-z]*\.auto\.qq\.com/.*',
                    r'http://[a-z]*\.house\.qq\.com/.*',
                    r'http://roll\.[a-z]*\.qq.com/.*',
                    r'http://[a-z]*\.qq.com/.*'
                  ]

    allow_shtml = [
                    r'http://[a-z]*\.auto\.qq\.com/a/.*\.s?html?$',
                    r'http://[a-z]*\.house\.qq\.com/a/.*\.s?html?$',
                    r'http://[a-z]*\.qq\.com/a/.*\.s?html?$'
                  ]

    allow_original = [
                        r'http://view\.news\.qq\.com/original/.*\.s?html?$',
                        r'http://[a-z]*\.qq\.com/original/.*\.s?html?$'
                     ]


    rules = [
                Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages),
                     callback='parse_shtml', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_original, deny=deny_pages),
                     callback='parse_original', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_shtml+allow_original+deny_pages),
                    process_links=linkfilter.index_filter)
            ]

    def parse_shtml(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.QQ_STORE, response.url)
        loader.add_value('path', path)

        loader.add_xpath('title', '//h1/text()')
        ps = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p[@style="TEXT-INDENT: 2em"]')
        if not ps:
            ps = response.xpath('//div[@id="Cnt-Main-Article-QQ"]/p')

        # old pages
        if not ps:
            loader.replace_xpath('title', '//div[@id="ArtTit"]/text()')
            ps = response.xpath('//div[@id="ArtCnt"]//p')
        if not ps:
            loader.replace_xpath('title', '//div[@id="ArticleTit"]/text()')
            ps = response.xpath('//div[@id="ArticleCnt"]//p')

        for p in ps:
            if p.xpath('./script'):
                continue
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()

    def parse_original(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.QQ_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//h1/text()')
        loader.add_xpath('text', '//div[@class="daoyu"]//div[@class="intr"]/text()')
        loader.add_xpath('text', '//div[@id="articleContent"]/h2/text()')
        loader.add_xpath('text', '//div[@id="articleContent"]/h3/text()')
        loader.add_xpath('text', '//div[@id="articleContent"]/p/text()')
        loader.add_xpath('text', '//div[@class="jieyu"]//text()')

        return loader.load_item()

