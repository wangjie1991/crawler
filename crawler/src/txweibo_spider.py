# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from txweibo.spiders.filters import WeiboBloomFilter
from txweibo.items import TxweiboItem, TxweiboLoader


class TxweiboSpider(CrawlSpider):
    name = 'txweibo'
    allowed_domains = ['t.qq.com']
    start_urls = ['http://t.qq.com/kaifulee']
    wbf = WeiboBloomFilter('txweibo')
    
    rules = [Rule(LinkExtractor(allow=(r'http://t.qq.com/[\w*\-?]*$', r'&pi=[0-9]*?')), 
                  callback='parse_item', follow=True, process_links=wbf.filter_html)
            ]
    
    def parse_item(self, response):
        loader = TxweiboLoader(item = TxweiboItem(), response = response)
        
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//title/text()')
        loader.add_xpath('text', '//div[contains(@class, "msgCnt")]//text()')
        
        return loader.load_item()

            fl = re.findall('&pi=([0-9]*?)&', item['url'])
            fn = 0
            if fl:
                fn = fl[0]
            else:
                fn = 0
            fn = '%s/%s.txt' % (path, fn)
            
