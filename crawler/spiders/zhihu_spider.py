# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    start_urls = ['http://www.zhihu.com/topic/19776749/questions']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('zhihu')
    allowed_domains = ['www.zhihu.com']

    deny_page = [
                    r'http://www\.zhihu\.com/question/\d+/answer/\d+$',
                    r'http://www.zhihu.com/people/.*$',
                    r'https://www\.zhihu\.com/question/\d+/answer/\d+$',
                    r'https://www.zhihu.com/people/.*$'
                ]
    allow_index = [ 
                    r'https://www\.zhihu\.com/.*',
                    r'http://www\.zhihu\.com/.*'
                  ]
    allow_shtml = [
                    r'https://www\.zhihu\.com/question/\d+$',
                    r'http://www\.zhihu\.com/question/\d+$'
                  ]

    rules = [
                # Rule(LinkExtractor(allow=allow_shtml, deny=deny_page), 
                Rule(LinkExtractor(allow=allow_shtml), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                # Rule(LinkExtractor(allow=allow_index, deny=allow_shtml+deny_page), 
                Rule(LinkExtractor(allow=allow_index, deny=allow_shtml), 
                     process_links=linkfilter.index_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item = TextItem(), response = response)

        path = self.pathextractor.zhihu(settings.ZH_STORE, response.url)
        loader.add_value('path', path)
        loader.add_value('title', '')

        loader.add_xpath('text', '//div[@id="zh-question-title"]//text()')
        loader.add_xpath('text', '//div[@id="zh-question-detail"]//text()')

        ps = response.xpath('//div[@class="zm-editable-content clearfix"]')
        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            loader.add_value('text', text)

        return loader.load_item()


