# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.items import TextItem, TextLoader


class BaiduMusicSpider(CrawlSpider):
    name = 'baidumusic'
    allowed_domains = ['music.baidu.com']
    start_urls = ['http://music.baidu.com/tag']
    pathextractor = PathExtractor()
#    linkfilter = LinkFilter('baidumusic')
    
    rules = [
                Rule(LinkExtractor(allow=(r'http://music.baidu.com/tag/.*')), callback='parse_item', follow=True)
                #Rule(LinkExtractor(allow=(r'http://news.sina.com.cn/.*?s?html')), callback='parse_item', follow=True, process_links=linkfilter.html_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.baidumusic(response.url)
        loader.add_value('path', path)

        loader.add_xpath('text', '//div[contains(@class, "song-item clearfix ")]//a//text()')
        
        return loader.load_item()

