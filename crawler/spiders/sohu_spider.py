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
                        'news.sohu.com'

                        'chuangke.sohu.com',
                        'auto.sohu.com',
                        '2sc.sohu.com',
                        'fashion.sohu.com',
                        'health.sohu.com',
                        'travel.sohu.com',
                        'learning.sohu.com',
                        'learning.sohu.com/liuxue',
                        'learning.sohu.com/gaokao.shtml',
                        'baobao.sohu.com',
                        'chihe.sohu.com',
                        'astro.sohu.com',
                        'gongyi.sohu.com',
                        'yule.sohu.com',
                        'music.sohu.com',
                        'app.sohu.com',
                        'www.focus.cn',
                        'esf.focus.cn/search',
                        'home.focus.cn',
                        'caipiao.sohu.com',
                        'city.sohu.com',
                      ]
    newsmaker_list
    deny_shtml = [news.sohu.com/matrix,
                    http://pic.xxxx
                  ]

    allow_index = [
                    r'http://[a-z]*\.sports\.sohu\.com/.*/$', 
                    r'http://[a-z]*\.sohu\.com/.*/$', 
                  ]

                        'star.news.sohu.com',
                        'digi.it.sohu.com',
                        'digi.it.sohu.com/mobile.shtml',
    allow_shtml = [
                    r'http://star\.news\.sohu\.com/[\d]*/.*\.s?html$', 
                    r'http://[a-z]*\.sohu\.com/[\d]*/.*\.s?html$'
                  ]

    allow_comnt = [
                    cul/history/book/
                    book.sohu.com/s2014/chenhuan/
                    r'http://[a-z]\.sohu\.com/s[\d]*/.*\.s?html$',
                    <div id="contentA">//<p>
                    <div class="area xxx clearfix">//<p>
                    r'http://star\.news\.sohu\.com/s[\d]*/.*\.s?html$', 
                    <div id="content">//<p>
                  ]
 

    rules = [
                Rule(LinkExtractor(allow=allow_shtml),
                     callback='parse_item', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_original),
                     callback='parse_original', follow=True, 
                     process_links=linkfilter.html_filter),
                Rule(LinkExtractor(allow=allow_index, deny=allow_a+allow_original),
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


