# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from tianya.spiders.filters import MyBloomFilter
from tianya.items import TianyaItem, TianyaLoader

class TianyaSpider(CrawlSpider):
    name = 'tianya'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/']
    mbf = MyBloomFilter('tianya')

    rules = [Rule(LinkExtractor(allow=(r'http://bbs.tianya.cn/post.*')),
                  callback='parse_item', follow=True, process_links=mbf.filter_html),
             Rule(LinkExtractor(allow=(r'http://bbs.tianya.cn/.*')),
                  process_links=mbf.filter_index)]

    def parse_item(self, response):
        loader = TianyaLoader(item = TianyaItem(), response = response)

        loader.add_value('url', response.url)
        loader.add_xpath('text', '//div[contains(@class, "bbs-content")]//text()')

        return loader.load_item()
