# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader
from crawler import settings


class TiebaSpider(CrawlSpider):
    name = 'tieba'
    start_urls = ['http://tieba.baidu.com/']
    #start_urls = ['http://tieba.baidu.com/f?kw=%BF%EC%C0%D6%B4%F3%B1%BE%D3%AA']
    pathextractor = PathExtractor()
    linkfilter = LinkFilter('tieba')
    pat_fnd = re.compile(r'"content":"(\u.*?)",')
    pat_sub = re.compile(r'<.*?>')

    allowed_domains = ['tieba.baidu.com']

    deny_pages = []
    #allow_index = [r'http://tieba\.baidu\.com/f[/\?].*?']
    allow_index = [r'http://tieba\.baidu\.com/.*/$']
    allow_shtml = [
                    r'http://tieba\.baidu\.com/p/[0-9]*$', 
                    r'http://tieba\.baidu\.com/p/[0-9]*\?pn=[0-9]*$'
                  ]

    rules = [
                Rule(LinkExtractor(allow=allow_shtml), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_shtml), 
                     process_links=linkfilter.index_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item = TextItem(), response = response)

        path = self.pathextractor.tieba(settings.TB_STORE, response)
        loader.add_value('path', path)
        loader.add_value('title', '')

        # main content
        #loader.add_xpath('text', '//div[re:test(@class, "d_post_content j_d_post_content[\s\S]*")]/text()')
        loader.add_xpath('text', '//div[contains(@class, "d_post_content j_d_post_content")]/text()')
        # comment content
        comnt_list = self.pat_fnd.findall(response.body.decode('utf-8'))
        for comnt in comnt_list:
            text = self.pat_sub.sub('', comnt)
            text = text.decode('raw_unicode_escape')
            # or text = eval('u"%s"' % text)
            loader.add_value('text', text)

        return loader.load_item()


