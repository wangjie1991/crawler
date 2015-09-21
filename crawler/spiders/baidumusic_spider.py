# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import BaiduMusicFilter
from crawler.items import TextItem, TextLoader


class BaiduMusicSpider(CrawlSpider):
    name = 'baidumusic'
    allowed_domains = ['music.baidu.com']
    start_urls = ['http://music.baidu.com/tag']
    pathextractor = PathExtractor()
    linkfilter = BaiduMusicFilter('baidumusic')
    
    rules = [
#Rule(LinkExtractor(allow=(r'http://music.baidu.com/tag/.*')), callback='parse_item', follow=True)
                Rule(LinkExtractor(allow=(r'http://music.baidu.com/tag/.*')), callback='parse_item', follow=True, process_links=linkfilter.url_filter)
            ]
    
    def parse_item(self, response):
        loader = TextLoader(item=TextItem(), response=response)

        path = self.pathextractor.baidumusic(response.url)
        loader.add_value('path', path)

        text = self.getText(response)
        loader.add_value('text', text)
        
        return loader.load_item()

    def getText(self, response):
        text = ''

        items = response.xpath('//div[contains(@class, "song-item clearfix ")]')
        for item in items:
            songs = item.xpath('.//span[contains(@class, "song-title")]/a//text()').extract()
            singers = item.xpath('.//span[contains(@class, "singer")]//text()').extract()
            albums = item.xpath('.//span[contains(@class, "album-title")]/a//text()').extract()

            if not songs:
                continue
            song = songs[0]

            singer = ''
            if singers:
                for s in singers:
                    singer = singer + s
            singer = singer.strip()

            album = ''
            if albums:
                album = albums[0]

            t = '<item>\n\t<song>%s</song>\n\t<singer>%s</singer>\n\t<album>%s</album>\n</item>\n' % (song, singer, album)
            text = text + t

        return text

