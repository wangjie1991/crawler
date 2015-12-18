# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy import log
from crawler.spiders.pathextractor import PathExtractor
from crawler.items import TextItem, TextLoader
from crawler import settings


class SnwbLogin():
    start_urls =[]

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    def login(self, start_urls):
        self.start_urls = start_urls
        url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
        return scrapy.Request(url, callback=self.postData, dont_filter=True)

    def postData(self, response):
        action = response.xpath('//form/@action').extract()[0]
        pwdname = response.xpath('//input[@type="password"]/@name').extract()[0]
        vk = response.xpath('//input[@name="vk"]/@value').extract()[0]

        data = {
            'mobile': self.username,
            pwdname: self.pwd,
            'remember': 'on',
            # 'backURL': 'http://weibo.cn/',
            'backURL': 'http%3A%2F%2Fweibo.cn%2F',
            'backTitle': '微博',
            'tryCount': '',
            'vk': vk,
            'submit': '登录'
            # 'encoding': 'utf-8'
        }

        url = 'http://login.weibo.cn/login/' + action
        return scrapy.FormRequest(url, formdata=data, callback=self.startCrawl, dont_filter=True)

    def startCrawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)


class SnwbSpider(scrapy.Spider):
    name = 'snwb'
    pathextractor = PathExtractor()
    snwblogin = SnwbLogin('mononogy@sina.cn', 'amethyst')
    start_urls = ['http://weibo.cn/gzmtr']

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

        next_page = self.load_next(response)
        if next_page:
            yield scrapy.Request(next_page, dont_filter=True)

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


