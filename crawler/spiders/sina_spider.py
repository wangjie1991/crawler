# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader


class SinaSpider(CrawlSpider):
    name = 'sina'
    linkfilter = LinkFilter('sina')
    start_urls = ['http://sina.com.cn']

    allowed_domains = [
                        'gongyi.sina.com.cn'
                        'lottery.sina.com.cn'
                        'collection.sina.com.cn'
                        'health.sina.com.cn'
                        'book.sina.com.cn'
                        'jiaju.sina.com.cn'
                        'baby.sina.com.cn', 
                        'edu.sina.com.cn', 
                        'fashion.sina.com.cn', 
                        'history.sina.com.cn', 
                        'zhuanlan.sina.com.cn', 
                        'yue.sina.com.cn'
                        'ent.sina.com.cn', 
                        'run.sina.com.cn'
                        'sports.sina.com.cn', 
                        'shiqu.sina.com.cn'
                        'mobile.sina.com.cn'
                        'digi.sina.com.cn'
                        'chuangye.sina.com.cn'
                        'tech.sina.com.cn', 
                        'finance.sina.com.cn', 
                        'news.sina.com.cn' 
                      ]

    deny_pages = [
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
                    r'http://news.jiaju.sina.com.cn/.*'
                    r'http://kid\.baby\.sina\.com\.cn/'
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
                Rule(LinkExtractor(allow=allow_index, deny=deny_pages), 
                     process_links=linkfilter.index_filter),
                Rule(LinkExtractor(allow=allow_shtml, deny=deny_pages), 
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

#        path = PathExtractor.parse_sina(response.url)
        loader.add_value('path', '')

        loader.add_xpath('text', '//h1/text()')
        
        t1 = response.xpath('//div[contains(@id, "artibody")]//p//text()')
        if t1:
            # <p>中会有<strong>修饰文本，也为了最大匹配artibody，保证<p>匹配成功
            loader.add_xpath('text', '//div[contains(@id, "artibody")]//p//text()')
        elif t2:
            # <div id=article>内一些<p>会在里层，而且这里匹配失败会全匹配<p>，容易引入js杂料，所以这里需要匹配最大化
            # 早期网页中一般没有将重要文本放入<p>里层，里层反而有js等。
            loader.add_xpath('text', '//div[contains(@id, "article")]//p/text()')
        
        return loader.load_item()


