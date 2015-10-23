# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy import log
from crawler.spiders.pathextractor import PathExtractor
from crawler.spiders.linkfilter import LinkFilter
from crawler.spiders.snwb_login import SnwbLogin
from crawler.items import TextItem, TextLoader
from crawler import settings


class SnwbSpider(scrapy.Spider):
    name = 'snwb'
    start_urls = ['http://weibo.cn/kaifulee']
    pathextractor = PathExtractor()
    #linkfilter = LinkFilter('snwb')
    snwblogin = SnwbLogin('mononogy@sina.cn', 'amethyst')

    allowed_domains = [ 
                        'login.weibo.cn',
                        'newlogin.sina.cn', 
                        'passport.weibo.com', 
                        'weibo.cn'
                      ]

    def start_requests(self):
        yield self.snwblogin.login(self.start_urls)

    def parse(self, response):
        loader = TextLoader(item=TextItem(), response=response)
        path = self.pathextractor.weibo(settings.SNWB_STORE, response.url)
        loader.add_value('path', path)
        self.load_text(response, loader)
        item = loader.load_item()
        yield item

        deny_serv = self.deny_serv(response)
        if deny_serv:
            yield self.snwblogin.login([response.url])
        else:
            next_page = self.load_next(response)
            #if next_page and ('text' in item):
            if next_page:
                log.msg('next page')
                yield scrapy.Request(next_page, dont_filter=True)
            else:
                follow = self.load_follow(response)
                log.msg('follow')
                log.msg(follow)
                yield scrapy.Request(follow, callback=self.parse_follow)

    def load_text(self, response, loader):
        ctt_text = ''
        dtt_text = ''
        dc_list = response.xpath('//div[@class="c"]')

        for dc in dc_list:
            dd_list = dc.xpath('./div')
            if not dd_list:
                continue

            ctt_list = dd_list[0].xpath('./span[@class="ctt"]//text()').extract()
            if ctt_list:
                ctt_text = ''.join(ctt_list)
                ctt_text = ctt_text.replace('@', '')
                ctt_text = ctt_text.replace('#', '')
                ctt_text = ctt_text.replace('//', '')
                loader.add_value('text', ctt_text)

            dtt_list = dd_list[-1].xpath('.//text()').extract()
            if dtt_list:
                dtt_text = ''.join(dtt_list)
                idxl_str = '转发理由:'.decode('utf-8')
                idxr_str = '赞['.decode('utf-8')
                idxl = dtt_text.find(idxl_str)
                idxr = dtt_text.rfind(idxr_str)
                if (idxl != -1) and (idxr != -1):
                    dtt_text = dtt_text[ idxl + len(idxl_str) : idxr ]
                    dtt_text = dtt_text.replace('@', '')
                    dtt_text = dtt_text.replace('#', '')
                    dtt_text = dtt_text.replace('//', '')
                    loader.add_value('text', dtt_text)

    def deny_serv(self, response):
        deny = False
        label = '还没发过微博'.decode('utf-8')
        ts = response.xpath('//div[@class="c"]/text()').extract()
        if ts and (ts[0].find(label) != -1):
            deny = True
        return deny

    def load_next(self, response):
        links = response.xpath('//div[@class="pa"]//a/@href').extract()
        texts = response.xpath('//div[@class="pa"]//text()').extract()
        if (not links) or (not texts):
            return None

        link = links[0]
        text = texts[0]
        if (text != '下页'.decode('utf-8')):
            return None

        link = 'http://weibo.cn' + link
        return link

    def load_follow(self, response):
        link = response.xpath('//div[@class="tip2"]/a/@href').extract()[0]
        link = 'http://weibo.cn' + link
        return link

    def parse_follow(self, response):
        follows = response.xpath('//table')
        for follow in follows:
            link = follow.xpath('//a/@href').extract()[0]
            req = scrapy.Request(link, dont_filter=True)
            yield req

        next_follow = self.load_next(response)
        if next_follow:
            req = scrapy.Request(next_follow, callback=self.parse_follow)
            yield req


