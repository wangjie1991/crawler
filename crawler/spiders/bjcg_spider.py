# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings

class BjcgSpider(CrawlSpider):
    name = 'bjcg'
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('bjcg')
    pat_text = re.compile(r'&[a-z]*?;')

    start_urls = ['http://www.bjcg.gov.cn']
    allowed_domains = ['www.bjcg.gov.cn']
    deny_pages = [r'http://www\.bjcg\.gov\.cn/zt/ssjnw/.*']
    allow_shtml = [r'http://www\.bjcg\.gov\.cn/.*']
 
    rules = [
                Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages),
                     callback='parse_shtml', follow=True, 
                     process_links=linkfilter.html_filter)
            ]

    def parse_shtml(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.host(settings.BJCG_STORE, response.url)
        loader.add_value('path', path)
        loader.add_xpath('title', '//div[@class="main_xl_bt"]/text()')

        ps = response.xpath('//div[@class="main_xl_center"]//p')
        for p in ps:
            ts = p.xpath('.//text()').extract()
            text = ''.join(ts)
            text = self.pat_text.sub('', text)
            loader.add_value('text', text)

        return loader.load_item()


