# -*- coding: utf-8 -*-

import scrapy
import re
import logging
from sina_weibo.spiders.filters import SinaWeiboBloomFilter
from sina_weibo.spiders.login import Login
from sina_weibo.items import SinaWeiboItem, SinaWeiboLoader


class SinaWeiboSpider(scrapy.Spider):
    name = 'sina_weibo'
    allowed_domains = ['weibo.cn', 'login.sina.com.cn']
    start_urls = ['http://weibo.cn/kaifulee']

    re_text1 = re.compile(r'WB_text([\s\S]*?)div')
    re_text2 = re.compile(r'<([\s\S]*?)>')
    re_text3 = re.compile(r'\s+')
    re_link1 = re.compile(r'href=\\?"(.*?)\\?"')
    re_link2 = re.compile(r'http://weibo.com/[\w*\-?]*$')

    bf = SinaWeiboBloomFilter('sina_weibo')
    login = Login('mononogy@sina.cn', 'amethyst', start_urls)

    def start_requests(self):
        yield self.login.prelogin()

    def parse(self, response):
        body = response.body.decode('utf-8')
        text = self.getText(body)

        loader = SinaWeiboLoader(item=SinaWeiboItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//title/text()')
        loader.add_value('text', text)
        yield loader.load_item()

        if text:
            link_list = self.getLink(response)
            for link in link_list:
                yield link


    def getText(self, body):
        WB_text = self.re_text1.findall(body)
        text_list = []

        for text in WB_text:
            text = text[text.find('>')+1 : text.rfind('<')]
            text = self.re_text2.sub(' ', text)
            rc_list = ['@', '#', '\\r', '\\n', '\\t','\\/', '\\']
            for rc in rc_list:
                text = text.replace(rc, ' ')
            text = self.re_text3.sub(' ', text)
            text_list.append(text)

        return text_list


    def getLink(self, response):
        url_set = set()
        req_list = []

        # find other user link in current page
        page_url_list = self.re_link1.findall(response.body.decode('utf-8'))
        for page_url in page_url_list:
            #去除转义字符
            page_url = page_url.replace('\\', '')
            #相对路径
            if page_url[0] == '/':
                page_url = 'http://weibo.com' + page_url
            if self.re_link2.match(page_url):
                url_set.add(page_url)

        # get next webpage from current page
        url = response.url
        index1 = url.find('page=')
        # http://weibo.com/kaifulee
        if self.re_link2.match(url):
            #url = url + '?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=2#feedtop'
            url = url + '?page=2'
            url_set.add(url)
        # http://weibo.com/kaifulee?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=5#feedtop
        elif index1 != -1:
            index2 = url.find('#', index1)
            if index2 == -1:
                page_id = 1 + int(url[index1+5:])
                url = url[:index1+5] + str(page_id)
            else:
                page_id = 1 + int(url[index1+5:index2])
                url = url[:index1+5] + str(page_id) + url[index2:]
            url_set.add(url)
        else:
            pass

        # bloom filter
        url_set = self.bf.filter_html(url_set)

        for next_url in url_set:
            #if re.match(r'http://weibo.com/kaifulee', next_url):
            req_list.append(scrapy.Request(next_url, callback=self.parse))

        return req_list
