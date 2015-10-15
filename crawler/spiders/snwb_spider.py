# -*- coding: utf-8 -*-

import scrapy
import re
import logging
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.spiders.snwblogin import SnwbLogin
from crawler.items import WeiboItem, WeiboLoader
from crawler import settings


class SnwbSpider(scrapy.Spider):
    name = 'snwb'
    allowed_domains = ['weibo.cn', 'login.sina.com.cn', 'weibo.com']
    start_urls = ['http://weibo.cn/kaifulee']
    
    pathextractor = PathExtractor()
#linkfilter = Wy163Filter('wy163')
    re_http = re.compile(r'http://[\w\./]*?')
    login = SnwbLogin('mononogy@sina.cn', 'amethyst', start_urls)

    def start_requests(self):
        yield self.login.prelogin()

    def parse(self, response):
        loader = WeiboLoader(item=WeiboItem(), response=response)
        path = self.pathextractor.weibo(settings.SNWB_STORE, response.url)
        loader.add_value('path', path)
        self.load_text(response, loader)
        item = loader.load_item()
        yield item

        next_page = self.load_next(response)
        if next_page and ('text' in item):
            req = scrapy.Request(next_page, callback=self.parse)
            yield req;
        else:
            follow = self.load_follow(response)
            req = scrapy.Request(follow, callback=self.parse_follow)
            yield follow

    def load_text(self, response, loader):
        text = ''
        sep = ''
        ctt_text = ''
        dtt_text = ''
        dc_list = response.xpath('//div[contains(@class, "c")]')

        for dc in dc_list:
            dd_list = dc.xpath('./div')

            ctt_list = dd_list[0].xpath('./span[contains(@class, "ctt")]//text()').extract()
            if ctt_list:
                ctt_text = sep.join(ctt_list)
                ctt_text = ctt_text.replace('@', '')
                ctt_text = ctt_text.replace('//', '')
                ctt_text = self.re_http('', ctt_text)
                loader.add_value('text', ctt_text)

            dtt_list = dd_list[-1].xpath('.//text()').extract()
            if dtt_list:
                dtt_text = sep.join(dtt_list)
                idxl_str = '转发理由:'
                idxr_str = '赞['
                idxl = dtt_text.find(idxl_str)
                idxr = dtt_text.rfind(idxr_str)
                if (idxl != -1) and (idxr != -1):
                    dtt_text = dtt_text[ idxl + len(idxl_str) : idxr ]
                    dtt_text = dtt_text.replace('@', '')
                    dtt_text = dtt_text.replace('//', '')
                    dtt_text = self.re_http('', dtt_text)
                    loader.add_value('text', dtt_text)

    def load_next(self, response):
        links = response.xpath('//div[contains(@class, "pa")]//a/@href').extract()
        texts = response.xpath('//div[contains(@class, "pa")]//text()').extract()
        if (not links) or (not texts):
            return None

        link = links[0]
        text = texts[0]
        if (text != '下页'):
            return None

        link = 'http://weibo.cn' + link
        return link

    def load_follow(self, response):
        link = response.xpath('//div[contains(@class, "tip2")]/a/@href').extract()[0]
        link = 'http://weibo.cn' + link
        return link

    def parse_follow(self, response):
        follows = response.xpath('//table')
        for follow in follows:
            link = follow.xpath('//a/@href').extract()[0]
            req = scrapy.Request(link, callback=self.parse)
            yield req

        next_follow = self.load_next(response)
        if next_follow:
            req = scrapy.Request(next_follow, callback=self.parse_follow)
            yield req


