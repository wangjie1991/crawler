# -*- coding: utf-8 -*-

import scrapy


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
            #'backURL': 'http://weibo.cn/',
            'backURL': 'http%3A%2F%2Fweibo.cn%2F',
            'backTitle': '微博',
            'tryCount': '',
            'vk': vk,
            'submit': '登录'
            #'encoding': 'utf-8'
        }

        url = 'http://login.weibo.cn/login/' + action
        return scrapy.FormRequest(url, formdata=data, callback=self.startCrawl, dont_filter=True)

    def startCrawl(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)


